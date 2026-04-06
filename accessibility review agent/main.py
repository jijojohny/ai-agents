"""
Accessibility Review Agent — UX/UI descriptions to a11y findings (informal).
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
from schemas import A11yReviewReply
from tools import get_a11y_review_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are A11yReviewAgent. You review described UIs for accessibility barriers.

## Rules
1. You do not see the real app—work from the user’s description or pasted structure.
2. Be specific: component, barrier, severity, fix. Avoid vague “make it accessible.”
3. This is **not** a certified WCAG audit; recommend axe/Lighthouse/manual screen reader tests.
4. Use tools for checklist prompts when useful.
5. If JSON is requested, end with:
   {"summary":"","issues":[{"area":"","issue":"","severity":"","recommendation":""}],"quick_wins":[],"testing_suggestions":[],"disclaimer":"Not a formal WCAG audit; validate with experts and automated tools."}
"""


class AccessibilityReviewAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.25,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_a11y_review_tools()
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
        structured = self._parse(c)
        return {"message": t, "messages": msgs, "content": c, "structured": structured}

    def _parse(self, content: str) -> Optional[A11yReviewReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return A11yReviewReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("ACCESSIBILITY REVIEW RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Accessibility Review Agent")
    p.add_argument("--provider", default=os.getenv("A11Y_REVIEW_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.25)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = AccessibilityReviewAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or (
                "Modal checkout: no focus trap, close button icon-only, error text turns red only."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = AccessibilityReviewAgent(provider=os.getenv("A11Y_REVIEW_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat("Data table with sortable columns but headers not associated on mobile.", verbose=True)
    )


if __name__ == "__main__":
    main()
