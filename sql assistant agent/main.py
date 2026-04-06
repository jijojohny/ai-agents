"""
SQL Assistant Agent — read-only SQL from natural language + schema hints.
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
from schemas import SQLAssistantReply
from tools import get_sql_assistant_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are SQLAssistantAgent. You write **read-only** SQL and explain it.

## Rules
1. Default to **SELECT** or **WITH** queries only. Refuse to author destructive DDL/DML.
2. If the user’s schema is incomplete, state assumptions explicitly.
3. Warn about SQL injection risks; recommend bound parameters in application code.
4. Use tools for policy reminders when relevant.
5. If JSON is requested, end with:
   {"dialect":"postgres","intent_summary":"","sql":"","assumptions":[],"safety_notes":[]}
"""


class SQLAssistantAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.15,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_sql_assistant_tools()
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

    def _parse(self, content: str) -> Optional[SQLAssistantReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return SQLAssistantReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("SQL ASSISTANT RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="SQL Assistant Agent")
    p.add_argument("--provider", default=os.getenv("SQL_ASSISTANT_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.15)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = SQLAssistantAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or (
                "Postgres: tables users(id, email, created_at), orders(id, user_id, amount, created_at). "
                "Top 10 users by revenue last 30 days."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = SQLAssistantAgent(provider=os.getenv("SQL_ASSISTANT_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat("SQLite: explain how to dedupe rows keeping latest by updated_at.", verbose=True)
    )


if __name__ == "__main__":
    main()
