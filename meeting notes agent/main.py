"""
Meeting Notes Agent - turns rough notes into clean summaries and action items.
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
from schemas import MeetingNotesReply
from tools import get_meeting_notes_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are MeetingNotesAgent, specialized in concise meeting synthesis.

## Rules
1. Convert messy notes into a clear structure: summary, decisions, action items.
2. Action items should include owner and due date when provided.
3. If details are missing, call it out explicitly instead of inventing facts.
4. Use tools when helpful: extract_action_items and detect_risks.
5. When asked for JSON output, end with:
   {"summary":"...", "decisions":[], "action_items":[],"risks":[]}
"""


class MeetingNotesAgent:
    """LangChain meeting notes assistant with extraction tools."""

    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_meeting_notes_tools()
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

        structured = self._try_parse_structured(content)
        return {
            "message": user_text,
            "messages": messages,
            "content": content,
            "structured": structured,
        }

    def _try_parse_structured(self, content: str) -> Optional[MeetingNotesReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return MeetingNotesReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("MEETING NOTES RESULT")
        print("=" * 70)
        print(f"Message: {result.get('message', 'N/A')}")
        print("-" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print("Structured:", result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Meeting Notes Agent")
    parser.add_argument(
        "--provider",
        default=os.getenv("MEETING_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None, help="Model id (optional)")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument(
        "--message",
        "-m",
        default=None,
        help="Raw meeting notes text",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = MeetingNotesAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "Sprint sync notes: API delay by 3 days. Priya owns fix. QA starts Monday. "
        "Decision: postpone release by one week."
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = MeetingNotesAgent(provider=os.getenv("MEETING_AGENT_PROVIDER", "openai"))
    result = agent.chat(
        message="Summarize notes and list action items with owners: Team agreed to cut scope.",
        verbose=True,
    )
    agent.print_result(result)


if __name__ == "__main__":
    main()
