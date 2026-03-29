"""
Adversarial Review Agent — multi-phase analyst / red team / blue team / chair synthesis.
"""
from __future__ import annotations

import argparse
import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from llm_factory import build_chat_model
from orchestrator import run_adversarial_review
from tools import get_adversarial_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

CHAT_SYSTEM = """You are the Adversarial Review assistant. For deep analysis, tell the user they can run the CLI with --deep for the full multi-phase pipeline.
You can use tools to show review dimensions or assumption checklists. Be concise."""


class AdversarialReviewAgent:
    """
    - `chat`: lightweight tool-calling agent for rubrics and Q&A.
    - `run_deep_review`: four-phase orchestration (Analyst → Red → Blue → Chair JSON).
    """

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
        self.tools = tools if tools is not None else get_adversarial_tools()
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=CHAT_SYSTEM,
        )

    def chat(self, message: str, verbose: bool = False) -> dict:
        user_text = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        result = self.agent.invoke({"messages": [HumanMessage(content=user_text)]})
        messages = result.get("messages", [])
        content = ""
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None) or str(last)
        return {"message": user_text, "messages": messages, "content": content}

    def run_deep_review(
        self,
        proposal: str,
        extra_context: str = "",
        verbose: bool = False,
    ) -> dict:
        return run_adversarial_review(
            self.llm,
            proposal=proposal,
            extra_context=extra_context,
            verbose=verbose,
        )

    def print_deep_result(self, result: dict) -> None:
        print("\n" + "=" * 70)
        print("ADVERSARIAL REVIEW (DEEP)")
        print("=" * 70)
        print("--- Analyst ---\n")
        print(result.get("analyst_markdown", ""))
        print("\n--- Red Team ---\n")
        print(result.get("red_team_markdown", ""))
        print("\n--- Blue Team ---\n")
        print(result.get("blue_team_markdown", ""))
        print("\n--- Chair (raw) ---\n")
        print(result.get("chair_raw", ""))
        if result.get("structured"):
            print("\n--- Structured ---\n")
            print(result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Adversarial Review Agent")
    parser.add_argument(
        "--provider",
        default=os.getenv("ADV_REVIEW_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument("--temperature", type=float, default=0.35)
    parser.add_argument(
        "--deep",
        action="store_true",
        help="Run 4-phase analyst/red/blue/chair pipeline (advanced)",
    )
    parser.add_argument(
        "--context",
        default="",
        help="Extra context for --deep (file path or inline text)",
    )
    parser.add_argument("--message", "-m", default=None)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = AdversarialReviewAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )

    if args.deep:
        prop = args.message or (
            "We will ship a public API that returns user email hashes for marketing partners "
            "with opt-out only in settings."
        )
        ctx = args.context
        if ctx and os.path.isfile(os.path.expanduser(ctx)):
            with open(os.path.expanduser(ctx), "r", encoding="utf-8", errors="replace") as f:
                ctx = f.read()
        r = agent.run_deep_review(proposal=prop, extra_context=ctx or "", verbose=args.verbose)
        agent.print_deep_result(r)
        return

    msg = args.message or (
        "List risk dimensions I should use to review a fintech onboarding flow."
    )
    out = agent.chat(message=msg, verbose=args.verbose)
    print(out.get("content", ""))


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = AdversarialReviewAgent(provider=os.getenv("ADV_REVIEW_AGENT_PROVIDER", "openai"))
    r = agent.run_deep_review(
        proposal="Add AI-generated legal terms updates without lawyer review weekly.",
        verbose=True,
    )
    agent.print_deep_result(r)


if __name__ == "__main__":
    main()
