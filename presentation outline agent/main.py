"""Presentation Outline Agent — slide storyline and one-line slide list."""
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
from schemas import DeckOutlineReply
from tools import get_presentation_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are PresentationOutlineAgent. Build conference or internal deck **outlines** from topic, length, audience.

Rules: no fabricated data; suggest where charts need real numbers from the user.
If JSON requested, end with:
{"title_options":[],"audience_and_goal":"","storyline_beats":[],"slides":[],"speaker_notes_hints":[],"closing_cta":""}
"""


class PresentationOutlineAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.45,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_presentation_tools()
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
                st = DeckOutlineReply(**json.loads(m.group()))
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
        ag = PresentationOutlineAgent(provider=os.getenv("PRESENTATION_OUTLINE_AGENT_PROVIDER", "openai"))
        ag.print_result(
            ag.chat(
                "20 min conference talk: why we migrated from REST to gRPC internally. Audience: backend engineers.",
                verbose=True,
            )
        )
        return
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("PRESENTATION_OUTLINE_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.45)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    ag = PresentationOutlineAgent(a.provider, a.model, a.temperature)
    ag.print_result(ag.chat(a.message or "10-slide internal QBR for infra cost trends.", verbose=a.verbose))


if __name__ == "__main__":
    main()
