"""
API Design Agent — REST-style sketches from product requirements.
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
from schemas import ApiDesignReply
from tools import get_api_design_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are APIDesignAgent. You help teams sketch **practical HTTP APIs** (usually REST-style JSON).

## Rules
1. Start from the user’s product requirements; ask for missing constraints (mobile, third parties, compliance).
2. Prefer **resource-oriented** URLs, clear verbs, consistent error shape, pagination strategy.
3. Call out **auth** (OAuth2 client credentials vs user tokens), **scopes**, and **PII** handling at a high level.
4. Use tools for status-code and idempotency reminders when useful.
5. If JSON is requested, end with:
   {"overview":"","resources":[],"endpoints":[],"auth_security":[],"errors_and_pagination":[],"versioning":"","open_questions":[]}
"""


class ApiDesignAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.3,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_api_design_tools()
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

    def _parse(self, content: str) -> Optional[ApiDesignReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return ApiDesignReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("API DESIGN RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="API Design Agent")
    p.add_argument("--provider", default=os.getenv("API_DESIGN_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.3)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = ApiDesignAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or (
                "Design a v1 JSON API for team workspaces: create workspace, invite by email, "
                "list members, remove member. OAuth2 bearer for users."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = ApiDesignAgent(provider=os.getenv("API_DESIGN_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Sketch endpoints for async job: submit job, poll status, cancel, fetch result URL.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
