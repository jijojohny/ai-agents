"""
Localization i18n Agent — message catalogs, locales, and localization plans.
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
from schemas import LocalizationI18nReply
from tools import get_localization_i18n_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are LocalizationI18nAgent. You help plan i18n and localization work.

## Rules
1. Do not invent official translations for trademarks or legal copy.
2. Prefer message keys with clear translator context.
3. Call out pluralization, RTL, and formatting early.
4. Use tools for checklist / anti-patterns when helpful.
5. If JSON is requested, end with:
   {"locales":[],"copy_inventory":[],"message_key_suggestions":[],
    "pluralization_notes":[],"formatting_notes":[],"glossary":[],
    "risks":[],"open_questions":[],"sample_json_catalog":null}
"""


class LocalizationI18nAgent:
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
        self.tools = tools if tools is not None else get_localization_i18n_tools()
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

    def _parse(self, content: str) -> Optional[LocalizationI18nReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return LocalizationI18nReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("LOCALIZATION I18N RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Localization i18n Agent")
    p.add_argument("--provider", default=os.getenv("LOCALIZATION_I18N_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.25)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = LocalizationI18nAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "Plan i18n for a checkout UI: 'Pay now', 'Items: {count}', order total. "
                "Locales: en-US, es-MX, ar-SA. Return JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = LocalizationI18nAgent(provider=os.getenv("LOCALIZATION_I18N_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Extract message keys from: Welcome back, {name}! You have {n} unread messages.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
