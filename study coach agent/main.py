"""
Study Coach Agent — flashcards, practice questions, and study hints from notes.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from llm_factory import build_chat_model
from schemas import StudyPackReply
from tools import get_study_coach_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are StudyCoachAgent. You turn notes or syllabi into study aids.

## Rules
1. Prefer clear flashcards (atomic facts, one idea per card).
2. Flag when content might be wrong or incomplete—don't invent citations.
3. Use tools when helpful: active_recall_prompts, pomodoro_study_block.
4. If JSON is requested, end with:
   {"topic_summary":"...","flashcards":[{"front":"...","back":"..."}],"practice_questions":[],"study_schedule_hint":[]}
"""


class StudyCoachAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.4,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_study_coach_tools()
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def chat(self, message: str, verbose: bool = False) -> Dict[str, Any]:
        user_text = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        result = self.agent.invoke({"messages": [HumanMessage(content=user_text)]})
        messages = result.get("messages", [])
        content = ""
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None) or str(last)
        structured = self._try_parse(content)
        return {
            "message": user_text,
            "messages": messages,
            "content": content,
            "structured": structured,
        }

    def _try_parse(self, content: str) -> Optional[StudyPackReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return StudyPackReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("STUDY COACH RESULT")
        print("=" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print(result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Study Coach Agent")
    p.add_argument(
        "--provider",
        default=os.getenv("STUDY_COACH_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.4)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    agent = StudyCoachAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "Make 8 flashcards from: TCP vs UDP — when to use each, reliability, headers, examples."
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = StudyCoachAgent(provider=os.getenv("STUDY_COACH_AGENT_PROVIDER", "openai"))
    agent.print_result(agent.chat("Exam in 5 days on JVM garbage collection basics.", verbose=True))


if __name__ == "__main__":
    main()
