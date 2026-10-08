"""
Onboarding Guide Agent — day-1 / week-1 / month-1 onboarding outlines.
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
from schemas import OnboardingGuideReply
from tools import get_onboarding_guide_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are OnboardingGuideAgent. You draft practical onboarding guides.

## Rules
1. Do not invent company policies, benefits, or legal requirements.
2. Make owners and checklists explicit; pace Day 1 / Week 1 / Month 1.
3. Use tools for structure and anti-patterns when helpful.
4. If JSON is requested, end with:
   {"audience":"","goals":[],"day_one":[],"first_week":[],"first_month":[],
    "checklist":[],"owner_roles":[],"risks":[],"markdown_guide":null}
"""


class OnboardingGuideAgent:
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
        self.tools = tools if tools is not None else get_onboarding_guide_tools()
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

    def _parse(self, content: str) -> Optional[OnboardingGuideReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return OnboardingGuideReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("ONBOARDING GUIDE RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Onboarding Guide Agent")
    p.add_argument("--provider", default=os.getenv("ONBOARDING_GUIDE_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.3)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = OnboardingGuideAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "Onboard a mid-level backend engineer at a 40-person SaaS. "
                "Stack: Python, Postgres, AWS. Return JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = OnboardingGuideAgent(provider=os.getenv("ONBOARDING_GUIDE_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat("Customer success hire onboarding for B2B SaaS. Include checklist. JSON.", verbose=True)
    )


if __name__ == "__main__":
    main()
