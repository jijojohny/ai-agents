"""
SEO Content Brief Agent — outlines and keyword-aware briefs without inventing SERP metrics.
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
from schemas import SEOContentBriefReply
from tools import get_seo_content_brief_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are SEOContentBriefAgent. You produce SEO content briefs for writers.

## Rules
1. Do not invent search volume, difficulty scores, or live SERP rankings.
2. Infer intent carefully; say when more keyword-tool data is needed.
3. Prefer helpful structure over keyword stuffing.
4. Use tools for checklist and quality red flags when helpful.
5. If JSON is requested, end with:
   {"primary_keyword":"","secondary_keywords":[],"search_intent":"",
    "title_options":[],"meta_description":null,"outline_h2":[],
    "people_also_ask":[],"internal_link_ideas":[],"risks_notes":[]}
"""


class SEOContentBriefAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.35,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_seo_content_brief_tools()
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

    def _parse(self, content: str) -> Optional[SEOContentBriefReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return SEOContentBriefReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("SEO CONTENT BRIEF RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="SEO Content Brief Agent")
    p.add_argument("--provider", default=os.getenv("SEO_CONTENT_BRIEF_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.35)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = SEOContentBriefAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "Brief for blog: primary keyword 'remote team onboarding checklist'. "
                "Audience: HR managers at mid-size SaaS. Return JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = SEOContentBriefAgent(provider=os.getenv("SEO_CONTENT_BRIEF_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Landing page brief for 'SOC 2 Type II compliance checklist' for startups. JSON please.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
