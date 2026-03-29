"""
Travel Planner Agent — day-by-day outlines from constraints (no live bookings).
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
from schemas import TravelPlanReply
from tools import get_travel_planner_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are TravelPlannerAgent. You suggest itineraries from user constraints.

## Rules
1. Do not invent real-time prices, openings, or visa rules—tell the user to verify on official sites and listings.
2. Offer flexible alternatives (rain plan, low-energy day).
3. Respect budget and mobility hints when provided.
4. Use tools when helpful: trip_constraint_checklist, jet_lag_quick_tips.
5. If JSON is requested, end with:
   {"trip_summary":"...","days":[{"day_label":"...","bullets":[]}],"budget_notes":[],"transport_tips":[],"safety_and_etiquette":[]}
"""


class TravelPlannerAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.45,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_travel_planner_tools()
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

    def _try_parse(self, content: str) -> Optional[TravelPlanReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return TravelPlanReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("TRAVEL PLAN RESULT")
        print("=" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print(result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Travel Planner Agent")
    p.add_argument(
        "--provider",
        default=os.getenv("TRAVEL_PLANNER_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.45)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    agent = TravelPlannerAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "4 days in Lisbon, mid-budget, love food and viewpoints, moderate walking."
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = TravelPlannerAgent(provider=os.getenv("TRAVEL_PLANNER_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat("3 days Tokyo first-timer, Shinjuku base, mix temples + neighborhoods.", verbose=True)
    )


if __name__ == "__main__":
    main()
