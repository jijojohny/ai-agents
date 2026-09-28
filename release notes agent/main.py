"""
Release Notes Agent — turn commits/PR bullets into customer-facing release notes.
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
from schemas import ReleaseNotesReply
from tools import get_release_notes_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are ReleaseNotesAgent. You rewrite engineering change lists into clear release notes.

## Rules
1. Only include changes present in the user's input; do not invent features.
2. Separate breaking changes and upgrade steps clearly.
3. Prefer user-facing language; keep PR numbers if provided.
4. Use tools for structure and changelog hygiene when helpful.
5. If JSON is requested, end with:
   {"version":null,"headline":"","highlights":[],"features":[],"fixes":[],
    "breaking_changes":[],"upgrade_notes":[],"known_issues":[],"markdown_body":""}
"""


class ReleaseNotesAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.3,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_release_notes_tools()
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def chat(self, message: str, verbose: bool = False) -> Dict[str, Any]:
        t = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        out = self.agent.invoke({"messages": [HumanMessage(content=t)]})
        msgs = out.get("messages", [])
        c = getattr(msgs[-1], "content", None) or str(msgs[-1]) if msgs else ""
        return {
            "message": t,
            "messages": msgs,
            "content": c,
            "structured": self._parse(c),
        }

    def _parse(self, content: str) -> Optional[ReleaseNotesReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return ReleaseNotesReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("RELEASE NOTES RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Release Notes Agent")
    p.add_argument("--provider", default=os.getenv("RELEASE_NOTES_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.3)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = ReleaseNotesAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "v2.4.0 commits:\n"
                "- add SSO via SAML (#812)\n"
                "- fix CSV export truncating UTF-8 (#801)\n"
                "- BREAKING: rename /api/v1/hooks to /api/v1/webhooks\n"
                "Write customer notes + JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = ReleaseNotesAgent(provider=os.getenv("RELEASE_NOTES_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Version 1.2.0: dark mode UI, faster search, fixed login timeout. Markdown + JSON.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
