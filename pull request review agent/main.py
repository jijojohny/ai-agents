"""
Pull Request Review Agent — constructive feedback from described or pasted changes.
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
from schemas import PRReviewReply
from tools import get_pr_review_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are PRReviewAgent. You write **constructive** pull-request reviews.

## Rules
1. Work from the user’s description, diff snippet, or commit message—do not claim you ran CI or saw private repos unless stated.
2. Separate **blocking** issues from **nits**; suggest concrete fixes and tests.
3. Call out **security**, **privacy**, **concurrency**, and **API compatibility** when relevant.
4. Use tools for tone/severity guidance when useful.
5. If JSON is requested, end with:
   {"summary":"","strengths":[],"comments":[{"file_or_area":"","severity":"","comment":""}],"test_and_qa_gaps":[],"security_and_privacy_notes":[],"merge_recommendation":"needs_follow_up"}
merge_recommendation one of: approve, request_changes, needs_follow_up, comment_only
"""


class PullRequestReviewAgent:
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
        self.tools = tools if tools is not None else get_pr_review_tools()
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

    def _parse(self, content: str) -> Optional[PRReviewReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return PRReviewReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("PR REVIEW RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Pull Request Review Agent")
    p.add_argument("--provider", default=os.getenv("PR_REVIEW_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.25)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = PullRequestReviewAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or (
                "PR adds retry loop around payment API without idempotency key. "
                "Also logs full card metadata in debug."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = PullRequestReviewAgent(provider=os.getenv("PR_REVIEW_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Refactor: extracted UserService; 400 lines moved, no tests updated.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
