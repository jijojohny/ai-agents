"""
Bug Report Agent - turns messy issue descriptions into actionable bug reports.
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
from schemas import BugReportReply
from tools import get_bug_report_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are BugReportAgent. You help reporters file clear, reproducible bug reports for engineering teams.

## Rules
1. Extract or infer: summary, environment, steps to reproduce, expected vs actual behavior.
2. Ask for missing critical details (version, OS, URL, account type) instead of guessing.
3. Use tools when helpful: classify_severity_hint for a rough priority signal; repro_template for a blank skeleton.
4. If the issue sounds like a security vulnerability, advise responsible disclosure (do not post public PoCs) and suggest contacting the vendor privately.
5. Strip or redact obvious secrets (tokens, passwords); tell the user if they pasted sensitive data.
6. If JSON is requested, end with:
   {"title":"...","summary":"...","steps_to_reproduce":[],"expected_behavior":"...","actual_behavior":"...","environment_notes":[],"severity_hint":"...","suggested_labels":[]}
"""


class BugReportAgent:
    """LangChain agent for structured bug reports."""

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
        self.tools = tools if tools is not None else get_bug_report_tools()
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

    def _try_parse_structured(self, content: str) -> Optional[BugReportReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return BugReportReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("BUG REPORT RESULT")
        print("=" * 70)
        print(f"Message: {result.get('message', 'N/A')}")
        print("-" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print("Structured:", result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Bug Report Agent")
    parser.add_argument(
        "--provider",
        default=os.getenv("BUG_REPORT_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None, help="Model id (optional)")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--message", "-m", default=None, help="Rough bug description")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = BugReportAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "The checkout button does nothing on iPhone Safari after the last deploy. "
        "Works on Chrome desktop."
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = BugReportAgent(provider=os.getenv("BUG_REPORT_AGENT_PROVIDER", "openai"))
    result = agent.chat(
        message="Turn this into a proper report: API returns 500 on /users when limit=0.",
        verbose=True,
    )
    agent.print_result(result)


if __name__ == "__main__":
    main()
