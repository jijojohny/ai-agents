"""
Voice Creation Agent - Generate speech audio from text with persona support.
"""
from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


@dataclass
class PersonaConfig:
    """Configuration for a voice persona."""

    voice: str
    style_hint: str


class VoiceGenerationResult(BaseModel):
    """Structured response after generating voice output."""

    person: str = Field(description="Persona used for generation")
    voice: str = Field(description="Underlying TTS voice name")
    output_path: str = Field(description="Generated audio file path")
    text_length: int = Field(description="Length of input text")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class VoiceCreationAgent:
    """Text-to-speech agent with multi-person persona support."""

    DEFAULT_PERSONAS: Dict[str, PersonaConfig] = {
        "narrator": PersonaConfig(voice="alloy", style_hint="clear neutral narrator voice"),
        "teacher": PersonaConfig(voice="sage", style_hint="warm and explanatory voice"),
        "podcast_host": PersonaConfig(voice="nova", style_hint="engaging and energetic host tone"),
        "calm_assistant": PersonaConfig(voice="shimmer", style_hint="calm and reassuring assistant tone"),
        "announcer": PersonaConfig(voice="echo", style_hint="confident public announcement style"),
    }

    def __init__(
        self,
        model_name: str = "gpt-4o-mini-tts",
        personas: Optional[Dict[str, PersonaConfig]] = None,
        output_dir: str = "outputs",
        persona_store_path: str = "personas.json",
    ):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is missing. Set it in .env.")

        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.personas = personas or dict(self.DEFAULT_PERSONAS)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.persona_store_path = Path(persona_store_path)
        self._load_custom_personas()

    def list_personas(self) -> Dict[str, Dict[str, str]]:
        """Return available personas and voice details."""
        return {
            name: {"voice": cfg.voice, "style_hint": cfg.style_hint}
            for name, cfg in self.personas.items()
        }

    def add_persona(self, name: str, voice: str, style_hint: str) -> None:
        """Add or overwrite a custom persona."""
        normalized_name = name.strip().lower().replace(" ", "_")
        if not normalized_name:
            raise ValueError("Persona name cannot be empty.")
        self.personas[normalized_name] = PersonaConfig(voice=voice, style_hint=style_hint)
        self._save_custom_personas()

    def remove_persona(self, name: str) -> bool:
        """Remove a non-default persona by name."""
        normalized_name = name.strip().lower().replace(" ", "_")
        if normalized_name in self.DEFAULT_PERSONAS:
            return False
        removed = self.personas.pop(normalized_name, None)
        if removed:
            self._save_custom_personas()
            return True
        return False

    def create_voice(
        self,
        text: str,
        person: str = "narrator",
        filename: Optional[str] = None,
        audio_format: str = "mp3",
    ) -> VoiceGenerationResult:
        """Generate audio from text for a selected persona."""
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        persona = self.personas.get(person)
        if not persona:
            available = ", ".join(sorted(self.personas.keys()))
            raise ValueError(f"Unknown person '{person}'. Available: {available}")

        output_name = filename or f"{person}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{audio_format}"
        output_path = self.output_dir / output_name

        prompt_text = (
            f"Speak naturally using a {persona.style_hint}. "
            f"Keep pronunciation clear and pacing balanced.\n\n{text.strip()}"
        )

        response = self.client.audio.speech.create(
            model=self.model_name,
            voice=persona.voice,
            input=prompt_text,
            format=audio_format,
        )
        response.stream_to_file(str(output_path))

        return VoiceGenerationResult(
            person=person,
            voice=persona.voice,
            output_path=str(output_path),
            text_length=len(text),
        )

    def create_voice_for_people(
        self,
        text: str,
        persons: List[str],
        audio_format: str = "mp3",
        filename_prefix: Optional[str] = None,
    ) -> List[VoiceGenerationResult]:
        """Generate audio for multiple personas with one text input."""
        if not persons:
            raise ValueError("At least one person must be provided.")

        results: List[VoiceGenerationResult] = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for person in persons:
            safe_person = person.strip().lower().replace(" ", "_")
            output_name = (
                f"{filename_prefix}_{safe_person}_{timestamp}.{audio_format}"
                if filename_prefix
                else f"{safe_person}_{timestamp}.{audio_format}"
            )
            result = self.create_voice(
                text=text,
                person=safe_person,
                filename=output_name,
                audio_format=audio_format,
            )
            results.append(result)
        return results

    def _load_custom_personas(self) -> None:
        """Load custom personas from JSON store if available."""
        if not self.persona_store_path.exists():
            return
        try:
            payload = json.loads(self.persona_store_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                return
            for name, config in payload.items():
                if not isinstance(config, dict):
                    continue
                voice = config.get("voice")
                style_hint = config.get("style_hint")
                if voice and style_hint:
                    self.personas[name] = PersonaConfig(voice=voice, style_hint=style_hint)
        except (json.JSONDecodeError, OSError):
            # Keep defaults if file is malformed or unreadable.
            return

    def _save_custom_personas(self) -> None:
        """Save only non-default personas into JSON store."""
        custom = {
            name: {"voice": cfg.voice, "style_hint": cfg.style_hint}
            for name, cfg in self.personas.items()
            if name not in self.DEFAULT_PERSONAS
        }
        self.persona_store_path.write_text(json.dumps(custom, indent=2), encoding="utf-8")

    def print_result(self, result: VoiceGenerationResult) -> None:
        """Pretty print generation output."""
        print("\n" + "=" * 70)
        print("VOICE CREATION RESULT")
        print("=" * 70)
        print(f"Person: {result.person}")
        print(f"Voice: {result.voice}")
        print(f"Output: {result.output_path}")
        print(f"Text length: {result.text_length}")
        print(f"Created at: {result.created_at}")
        print("=" * 70 + "\n")


def _build_cli_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Voice Creation Agent CLI")
    parser.add_argument("--text", help="Text to convert to speech")
    parser.add_argument("--text-file", help="Path to a text file to read input from")
    parser.add_argument("--person", default="narrator", help="Single persona name")
    parser.add_argument(
        "--persons",
        help="Comma-separated persona names for batch generation (overrides --person)",
    )
    parser.add_argument("--format", default="mp3", choices=["mp3", "wav", "opus", "aac", "flac"])
    parser.add_argument("--filename", help="Output filename for single-person generation")
    parser.add_argument("--filename-prefix", help="Prefix for batch output filenames")
    parser.add_argument("--list-personas", action="store_true", help="List available personas")
    parser.add_argument("--add-persona-name", help="Name for new persona")
    parser.add_argument("--add-persona-voice", help="Voice id for new persona")
    parser.add_argument("--add-persona-style", help="Style hint for new persona")
    parser.add_argument("--remove-persona", help="Remove a custom persona by name")
    return parser


def _resolve_text(args: argparse.Namespace) -> str:
    if args.text and args.text.strip():
        return args.text.strip()
    if args.text_file:
        return Path(args.text_file).read_text(encoding="utf-8").strip()
    raise ValueError("Provide --text or --text-file for generation.")


def main() -> None:
    """CLI entrypoint for voice generation."""
    parser = _build_cli_parser()
    args = parser.parse_args()
    agent = VoiceCreationAgent()

    if args.list_personas:
        print(json.dumps(agent.list_personas(), indent=2))
        return

    if args.add_persona_name or args.add_persona_voice or args.add_persona_style:
        if not (args.add_persona_name and args.add_persona_voice and args.add_persona_style):
            raise ValueError(
                "To add persona, provide --add-persona-name, --add-persona-voice, and --add-persona-style."
            )
        agent.add_persona(
            name=args.add_persona_name,
            voice=args.add_persona_voice,
            style_hint=args.add_persona_style,
        )
        print(f"Added persona: {args.add_persona_name}")
        return

    if args.remove_persona:
        removed = agent.remove_persona(args.remove_persona)
        if removed:
            print(f"Removed persona: {args.remove_persona}")
        else:
            print(f"Persona '{args.remove_persona}' was not removed (default or missing).")
        return

    text = _resolve_text(args)
    if args.persons:
        persons = [p.strip().lower().replace(" ", "_") for p in args.persons.split(",") if p.strip()]
        results = agent.create_voice_for_people(
            text=text,
            persons=persons,
            audio_format=args.format,
            filename_prefix=args.filename_prefix,
        )
        for result in results:
            agent.print_result(result)
        return

    result = agent.create_voice(
        text=text,
        person=args.person.strip().lower().replace(" ", "_"),
        filename=args.filename,
        audio_format=args.format,
    )
    agent.print_result(result)


if __name__ == "__main__":
    main()
