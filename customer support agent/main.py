"""
Customer Support Agent - drafts support replies with actionable next steps.
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
from schemas import SupportReply
from tools import get_customer_support_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are CustomerSupportAgent, a concise and empathetic support specialist.

## Rules
1. Identify the user's issue, urgency, and desired outcome before proposing steps.
2. Use tools when helpful: categorize_issue for ticket routing, and generate_refund_checklist for refund-like requests.
3. Keep replies practical: include exactly what the user should do next.
4. Never invent policy details. If missing data is needed, ask for it clearly.
5. When structured output is requested, end with JSON:
   {"issue_category":"...", "customer_message":"...", "next_actions":[],"escalation_needed":false}
"""


class CustomerSupportAgent:
    """LangChain customer support agent with basic ticketing tools."""

    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_customer_support_tools()
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

    def _try_parse_structured(self, content: str) -> Optional[SupportReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return SupportReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("CUSTOMER SUPPORT RESULT")
        print("=" * 70)
        print(f"Message: {result.get('message', 'N/A')}")
        print("-" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print("Structured:", result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Customer Support Agent")
    parser.add_argument(
        "--provider",
        default=os.getenv("SUPPORT_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None, help="Model id (optional)")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument(
        "--message",
        "-m",
        default=None,
        help="Customer issue text (if omitted, runs a short demo)",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = CustomerSupportAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "My order arrived damaged and I want a refund. What should I do next?"
    )
    r = agent.chat(message=msg, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = CustomerSupportAgent(provider=os.getenv("SUPPORT_AGENT_PROVIDER", "openai"))
    result = agent.chat(
        message="Draft a polite response to: 'I was charged twice for one order.'",
        verbose=True,
    )
    agent.print_result(result)


if __name__ == "__main__":
    main()
