"""Event Planning Agent — run-of-show and logistics from event brief."""
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
from schemas import EventPlanReply
from tools import get_event_planning_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are EventPlanningAgent. From constraints (format, length, audience, venue/virtual), produce a **run-of-show**, **phased timeline**, **logistics checklist**, and **risks/contingencies**.

Do not invent vendor contracts, budgets, or legal permits—flag unknowns. Respect stated times and time zones.

If JSON requested, end with:
{"event_summary":"","audience_and_goals":"","timeline_phases":[],"run_of_show":[],"logistics_checklist":[],"risks_contingencies":[]}
"""


class EventPlanningAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.45,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_event_planning_tools()
        self.agent = create_agent(model=self.llm, tools=self.tools, system_prompt=SYS)

    def chat(self, message: str, verbose: bool = False) -> Dict[str, Any]:
        t = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        out = self.agent.invoke({"messages": [HumanMessage(content=t)]})
        msgs = out.get("messages", [])
        c = getattr(msgs[-1], "content", None) or str(msgs[-1]) if msgs else ""
        st = None
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", c) or re.search(r"\{[\s\S]*\}", c)
            if m:
                st = EventPlanReply(**json.loads(m.group()))
        except Exception:
            pass
        return {"message": t, "messages": msgs, "content": c, "structured": st}

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70 + "\n" + r.get("content", "") + "\n")
        if r.get("structured"):
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def main() -> None:
    import sys

    if len(sys.argv) <= 1:
        ag = EventPlanningAgent(provider=os.getenv("EVENT_PLANNING_AGENT_PROVIDER", "openai"))
        ag.print_result(
            ag.chat(
                "Half-day internal hackathon kickoff: 9am–1pm, 80 people, one auditorium + breakout rooms.",
                verbose=True,
            )
        )
        return
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("EVENT_PLANNING_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.45)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    ag = EventPlanningAgent(a.provider, a.model, a.temperature)
    ag.print_result(
        ag.chat(a.message or "90-min webinar: product roadmap Q2, hybrid, UTC.", verbose=a.verbose)
    )


if __name__ == "__main__":
    main()
