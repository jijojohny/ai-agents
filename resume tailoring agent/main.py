"""
Resume Tailoring Agent — align resume content with a job description (honesty-first).
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
from schemas import ResumeTailorReply
from tools import get_resume_tailor_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are ResumeTailorAgent. You help candidates **reword and prioritize** resume content for a target role.

## Rules
1. **Never invent** employers, titles, dates, degrees, certifications, or metrics. Use placeholders like [your metric] or ask the user.
2. Reflect **real** overlap with the job description using the candidate’s supplied experience only.
3. Use tools for bullet structure and ATS readability tips when useful.
4. If JSON is requested, end with:
   {"role_alignment_summary":"","keywords_from_jd":[],"revised_bullets":[],"professional_summary_suggestion":"","gaps_or_questions":[],"integrity_note":"Only claim what you can defend in an interview."}
"""


class ResumeTailoringAgent:
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
        self.tools = tools if tools is not None else get_resume_tailor_tools()
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
        structured = self._parse(c)
        return {"message": t, "messages": msgs, "content": c, "structured": structured}

    def _parse(self, content: str) -> Optional[ResumeTailorReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return ResumeTailorReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("RESUME TAILORING RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Resume Tailoring Agent")
    p.add_argument("--provider", default=os.getenv("RESUME_TAILOR_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.35)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = ResumeTailoringAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or (
                "JD: Senior backend engineer, Python, Postgres, k8s. "
                "My bullets: Led API migration; cut p95 latency; mentored 2 juniors."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = ResumeTailoringAgent(provider=os.getenv("RESUME_TAILOR_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Paste JD + 3 current bullets; tailor for PM role without new false claims.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
