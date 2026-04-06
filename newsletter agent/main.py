"""
Newsletter Agent — subject lines, sections, and markdown drafts.
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
from schemas import NewsletterReply
from tools import get_newsletter_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are NewsletterAgent. You write engaging, honest email newsletters.

## Rules
1. Match brand voice, audience, and frequency the user describes.
2. One primary CTA; scannable layout.
3. Remind that real sends need legal footer, unsubscribe, and applicable compliance (CAN-SPAM, GDPR).
4. Use tools when useful for structure.
5. If JSON is requested, end with:
   {"subject_lines":[],"preview_text":"","sections":[],"body_markdown":"","cta":"","unsubscribe_reminder":"Include compliant unsubscribe link in real sends."}
"""


class NewsletterAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.55,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_newsletter_tools()
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

    def _parse(self, content: str) -> Optional[NewsletterReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return NewsletterReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("NEWSLETTER RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Newsletter Agent")
    p.add_argument("--provider", default=os.getenv("NEWSLETTER_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.55)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = NewsletterAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or "Weekly dev newsletter: 3 links + one tip on CI caching.",
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = NewsletterAgent(provider=os.getenv("NEWSLETTER_AGENT_PROVIDER", "openai"))
    agent.print_result(agent.chat("Product launch email for waitlist: soft tone, one CTA.", verbose=True))


if __name__ == "__main__":
    main()
