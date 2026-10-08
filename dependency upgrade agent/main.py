"""
Dependency Upgrade Agent — plan package upgrades with tests and rollback notes.
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
from schemas import DependencyUpgradeReply
from tools import get_dependency_upgrade_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are DependencyUpgradeAgent. You plan dependency upgrades safely.

## Rules
1. Do not invent CVE IDs, fixed versions, or changelog entries the user did not provide.
2. Prefer incremental upgrade order, tests, and rollback notes.
3. Use tools for playbook and red flags when helpful.
4. If JSON is requested, end with:
   {"ecosystem":"","packages":[],"upgrade_order":[],"breaking_change_watchlist":[],
    "test_plan":[],"rollback_notes":[],"security_notes":[],"open_questions":[],"summary":null}
"""


class DependencyUpgradeAgent:
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
        self.tools = tools if tools is not None else get_dependency_upgrade_tools()
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

    def _parse(self, content: str) -> Optional[DependencyUpgradeReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return DependencyUpgradeReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("DEPENDENCY UPGRADE RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Dependency Upgrade Agent")
    p.add_argument("--provider", default=os.getenv("DEPENDENCY_UPGRADE_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = DependencyUpgradeAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message
            or (
                "npm: react 17 -> 18, react-router 5 -> 6. Plan upgrade order, tests, rollback. JSON."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = DependencyUpgradeAgent(
        provider=os.getenv("DEPENDENCY_UPGRADE_AGENT_PROVIDER", "openai")
    )
    agent.print_result(
        agent.chat(
            "pip: Django 4.2 LTS -> 5.0. List watchlist and test plan. Return JSON.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
