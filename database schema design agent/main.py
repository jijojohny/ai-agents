"""
Database Schema Design Agent — relational (and related) schema sketches from requirements.
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
from schemas import DatabaseSchemaDesignReply
from tools import get_database_schema_design_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are DatabaseSchemaDesignAgent. You design clear data models from product requirements.

## Rules
1. Prefer explicit assumptions when requirements are incomplete.
2. Suggest keys, FKs, indexes with justification—not cargo-cult indexes.
3. DDL sketches should be non-destructive CREATE suggestions; warn about production migrations.
4. Use tools for checklist / normalization tradeoffs when helpful.
5. If JSON is requested, end with:
   {"dialect":"postgres","overview":"","tables":[],"constraints_notes":[],
    "migration_notes":[],"open_questions":[],"ddl_sketch":null}
"""


class DatabaseSchemaDesignAgent:
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
        self.tools = tools if tools is not None else get_database_schema_design_tools()
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

    def _parse(self, content: str) -> Optional[DatabaseSchemaDesignReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return DatabaseSchemaDesignReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("DATABASE SCHEMA DESIGN RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Database Schema Design Agent")
    p.add_argument(
        "--provider",
        default=os.getenv("DATABASE_SCHEMA_DESIGN_AGENT_PROVIDER", "openai"),
    )
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = DatabaseSchemaDesignAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "Postgres schema for a multi-tenant SaaS: orgs, users, memberships, projects, "
                "and audit events. Include open questions. Return JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = DatabaseSchemaDesignAgent(
        provider=os.getenv("DATABASE_SCHEMA_DESIGN_AGENT_PROVIDER", "openai")
    )
    agent.print_result(
        agent.chat(
            "Design an e-commerce catalog: products, variants, inventory, orders. Dialect postgres. JSON.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
