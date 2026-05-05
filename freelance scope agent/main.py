"""Freelance Scope Agent — SOW-style bullets from a client brief (not legal advice)."""
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
from schemas import FreelanceScopeReply
from tools import get_freelance_scope_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are FreelanceScopeAgent. Turn rough client briefs into **structured scope drafts**: deliverables, milestones, assumptions, out-of-scope, risks/questions.

This is **not legal advice**. Do not invent dollar amounts, jurisdictions, or binding contract language. Flag items that need a lawyer or accountant.

If JSON requested, end with:
{"project_summary":"","deliverables":[],"milestones":[],"assumptions":[],"out_of_scope":[],"risks_open_questions":[],"payment_terms_notes":""}
"""


class FreelanceScopeAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.45,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_freelance_scope_tools()
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
                st = FreelanceScopeReply(**json.loads(m.group()))
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
        ag = FreelanceScopeAgent(provider=os.getenv("FREELANCE_SCOPE_AGENT_PROVIDER", "openai"))
        ag.print_result(
            ag.chat(
                "Client wants a small React dashboard for internal KPIs, 6-week max, they host on Azure.",
                verbose=True,
            )
        )
        return
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("FREELANCE_SCOPE_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.45)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    ag = FreelanceScopeAgent(a.provider, a.model, a.temperature)
    ag.print_result(
        ag.chat(a.message or "Logo refresh + brand guidelines PDF, async with marketing lead.", verbose=a.verbose)
    )


if __name__ == "__main__":
    main()
