"""
Job Description Writer Agent — draft inclusive, structured job postings.
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
from schemas import JobDescriptionReply
from tools import get_job_description_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are JobDescriptionWriterAgent. You draft clear, inclusive job descriptions.

## Rules
1. Do not invent salary numbers, visa sponsorship, or benefits the user did not provide.
2. Separate must-haves from nice-to-haves; keep requirements realistic for the seniority.
3. Prefer outcome-oriented responsibilities over buzzword stacks.
4. Use tools for structure and inclusive-language checks when helpful.
5. If JSON is requested, end with:
   {"title_options":[],"summary":"","responsibilities":[],"requirements_must":[],
    "requirements_nice":[],"compensation_notes":null,"inclusivity_notes":[],"open_questions":[]}
"""


class JobDescriptionWriterAgent:
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
        self.tools = tools if tools is not None else get_job_description_tools()
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

    def _parse(self, content: str) -> Optional[JobDescriptionReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return JobDescriptionReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("JOB DESCRIPTION WRITER RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Job Description Writer Agent")
    p.add_argument("--provider", default=os.getenv("JOB_DESCRIPTION_WRITER_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.35)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = JobDescriptionWriterAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "Write a mid-level backend engineer JD for a Series A fintech (hybrid, NYC). "
                "Stack: Python, Postgres, AWS. Return JSON at the end."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = JobDescriptionWriterAgent(
        provider=os.getenv("JOB_DESCRIPTION_WRITER_AGENT_PROVIDER", "openai")
    )
    agent.print_result(
        agent.chat(
            "Senior product designer JD for a B2B SaaS analytics product. Remote-first. Include open questions.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
