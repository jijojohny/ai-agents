"""Grant Proposal Agent — outline sections from RFP snippets and project facts."""
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
from schemas import GrantOutlineReply
from tools import get_grant_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are GrantProposalAgent. Draft **outlines** and section bullets for grant/RFP responses.

Rules: never invent budgets, credentials, or prior awards; use placeholders. Not legal/compliance advice.
If JSON requested, end with:
{"funder_fit_summary":"","problem_statement":"","objectives":[],"methods_workplan":[],"outcomes_and_metrics":[],"timeline_milestones":[],"budget_outline":[],"evaluation_risks":[],"disclaimer":"Drafting aid only—not legal, financial, or compliance approval. Match funder templates exactly."}
"""


class GrantProposalAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.3,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_grant_tools()
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
                st = GrantOutlineReply(**json.loads(m.group()))
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
        ag = GrantProposalAgent(provider=os.getenv("GRANT_PROPOSAL_AGENT_PROVIDER", "openai"))
        ag.print_result(
            ag.chat(
                "NSF-style: 2-year CS education outreach; need objectives and evaluation section bullets. No budget numbers yet.",
                verbose=True,
            )
        )
        return
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("GRANT_PROPOSAL_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.3)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    ag = GrantProposalAgent(a.provider, a.model, a.temperature)
    ag.print_result(ag.chat(a.message or "Private foundation LOI: climate resilience tool.", verbose=a.verbose))


if __name__ == "__main__":
    main()
