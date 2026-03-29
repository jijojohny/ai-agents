"""
Sales Outreach Agent — cold outreach, follow-ups, and short DMs with structure.
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
from schemas import OutreachReply
from tools import get_sales_outreach_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are SalesOutreachAgent. You draft concise, human outbound messages (email, LinkedIn).

## Rules
1. Never fabricate facts about the prospect or company—use placeholders if info is missing.
2. One clear CTA per message; avoid spammy hype and fake urgency.
3. Comply with CAN-SPAM / GDPR / local outreach norms conceptually: honest subject, easy to understand ask.
4. Use tools when helpful: classify_outreach_stage, outreach_length_guidelines.
5. If JSON is requested, end with:
   {"channel":"...","subject_or_hook":"...","body":"...","call_to_action":"...","follow_up_sequence":[],"research_questions":[]}
"""


class SalesOutreachAgent:
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
        self.tools = tools if tools is not None else get_sales_outreach_tools()
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
        structured = self._try_parse(content)
        return {
            "message": user_text,
            "messages": messages,
            "content": content,
            "structured": structured,
        }

    def _try_parse(self, content: str) -> Optional[OutreachReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return OutreachReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("SALES OUTREACH RESULT")
        print("=" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print(result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Sales Outreach Agent")
    p.add_argument(
        "--provider",
        default=os.getenv("SALES_OUTREACH_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.55)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    agent = SalesOutreachAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "Cold LinkedIn: I sell API monitoring to Series A SaaS. Prospect is VP Eng at a fintech. "
        "Write first touch + 2 follow-up ideas."
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = SalesOutreachAgent(provider=os.getenv("SALES_OUTREACH_AGENT_PROVIDER", "openai"))
    agent.print_result(agent.chat("Draft a short cold email for a data warehouse audit offer.", verbose=True))


if __name__ == "__main__":
    main()
