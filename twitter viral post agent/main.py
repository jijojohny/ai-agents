"""
Twitter / X Viral Post Agent - drafts high-retention posts and thread openers.
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
from schemas import ViralPostReply
from tools import get_twitter_viral_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are TwitterViralPostAgent. You help creators write posts for X (Twitter) that are clear, memorable, and shareable.

## Rules
1. Lead with a strong hook in the first line when possible (curiosity, contrast, specificity).
2. Prefer concrete details, numbers, and one vivid image over vague advice.
3. Offer single posts and optional thread outlines when the idea needs more room.
4. Match the user's voice if they describe it; otherwise default to direct, human, non-corporate.
5. Use tools when useful: check_post_length against 280 chars for standard accounts; list_viral_formats for structure ideas.
6. Safety: no harassment, hate, or targeted pile-ons. No false claims, medical/legal/financial advice presented as certainty. No coordinated inauthentic engagement tactics.
7. Avoid empty engagement bait ("like if you agree") and misleading clickbait.
8. If JSON is requested, end with:
   {"primary_post":"...","alternate_versions":[],"thread_outline":[],"hashtags":[],"posting_tips":[]}
"""


class TwitterViralPostAgent:
    """LangChain agent for X/Twitter-style post drafting."""

    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.75,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_twitter_viral_tools()
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def chat(self, message: str, verbose: bool = False) -> Dict[str, Any]:
        user_text = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")

        result = self.agent.invoke({"messages": [HumanMessage(content=user_text)]})
        messages = result.get("messages", [])
        content = ""
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None) or str(last)

        structured = self._try_parse_structured(content)
        return {
            "message": user_text,
            "messages": messages,
            "content": content,
            "structured": structured,
        }

    def _try_parse_structured(self, content: str) -> Optional[ViralPostReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return ViralPostReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("TWITTER / X VIRAL POST RESULT")
        print("=" * 70)
        print(f"Message: {result.get('message', 'N/A')}")
        print("-" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print("Structured:", result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Twitter / X Viral Post Agent")
    parser.add_argument(
        "--provider",
        default=os.getenv("TWITTER_VIRAL_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None, help="Model id (optional)")
    parser.add_argument("--temperature", type=float, default=0.75)
    parser.add_argument(
        "--message",
        "-m",
        default=None,
        help="Topic, angle, or draft to improve",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = TwitterViralPostAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "Write a viral-style X post about why most startup MVPs ship too late, "
        "with a contrarian hook. Keep under 280 characters for the main post."
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = TwitterViralPostAgent(provider=os.getenv("TWITTER_VIRAL_AGENT_PROVIDER", "openai"))
    result = agent.chat(
        message="Give me 3 hook options + one polished post about learning Rust in public.",
        verbose=True,
    )
    agent.print_result(result)


if __name__ == "__main__":
    main()
