"""
RFC Design Doc Agent — engineering RFCs and design-doc outlines.
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
from schemas import RfcDesignDocReply
from tools import get_rfc_design_doc_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are RfcDesignDocAgent. You draft engineering RFCs / design docs.

## Rules
1. Separate goals from non-goals; surface alternatives and risks.
2. Do not invent capacity numbers, SLAs, or vendor pricing.
3. Use tools for template sections and review focus when helpful.
4. If JSON is requested, end with:
   {"title":"","status":"draft","problem":"","goals":[],"non_goals":[],
    "proposal":"","alternatives":[],"risks":[],"open_questions":[],"markdown_rfc":null}
"""


class RfcDesignDocAgent:
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
        self.tools = tools if tools is not None else get_rfc_design_doc_tools()
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

    def _parse(self, content: str) -> Optional[RfcDesignDocReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return RfcDesignDocReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("RFC DESIGN DOC RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="RFC Design Doc Agent")
    p.add_argument("--provider", default=os.getenv("RFC_DESIGN_DOC_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.25)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = RfcDesignDocAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "RFC: move session store from Redis sticky cookies to signed JWT + short Redis blacklist. "
                "Include alternatives and open questions. Return JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = RfcDesignDocAgent(provider=os.getenv("RFC_DESIGN_DOC_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Design doc: introduce feature flags service for gradual rollout. Markdown + JSON.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
