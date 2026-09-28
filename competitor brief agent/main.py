"""
Competitor Brief Agent — structured competitive framing from user-provided notes.
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
from schemas import CompetitorBriefReply
from tools import get_competitor_brief_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are CompetitorBriefAgent. You synthesize competitive briefs from user notes.

## Rules
1. Do not invent market share, revenue, or confidential pricing.
2. Clearly separate facts the user provided from hypotheses.
3. Suggest verification steps for unverified claims.
4. Use tools for framework and ethics reminders when helpful.
5. If JSON is requested, end with:
   {"market_frame":"","competitors":[],"differentiation_angles":[],
    "risks_assumptions":[],"next_research_steps":[]}
"""


class CompetitorBriefAgent:
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
        self.tools = tools if tools is not None else get_competitor_brief_tools()
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

    def _parse(self, content: str) -> Optional[CompetitorBriefReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return CompetitorBriefReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("COMPETITOR BRIEF RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Competitor Brief Agent")
    p.add_argument("--provider", default=os.getenv("COMPETITOR_BRIEF_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.3)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = CompetitorBriefAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "Our product: developer API observability. Competitors mentioned: Datadog APM, "
                "New Relic, Honeycomb. We focus on OpenTelemetry-first pricing. Build a brief; JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = CompetitorBriefAgent(provider=os.getenv("COMPETITOR_BRIEF_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Category: AI meeting notes. Us vs Otter vs Fireflies. Notes only—no invented ARR. JSON.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
