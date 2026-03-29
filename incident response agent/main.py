"""
Incident Response Agent — multi-phase triage, technical, comms, and consolidated report.
"""
from __future__ import annotations

import argparse
import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from llm_factory import build_chat_model
from orchestrator import run_incident_pipeline
from tools import get_incident_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

CHAT_SYSTEM = """You help with incident response playbooks. Use tools for severity cheatsheets or postmortem outlines.
For a full multi-phase run, use CLI --run. Be concise; never claim live system access."""


class IncidentResponseAgent:
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
        self.tools = tools if tools is not None else get_incident_tools()
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

    def run_full_response(
        self,
        incident_description: str,
        extra_context: str = "",
        verbose: bool = False,
    ) -> dict:
        return run_incident_pipeline(
            self.llm,
            incident_description=incident_description,
            extra_context=extra_context,
            verbose=verbose,
        )

    def print_full_result(self, result: dict) -> None:
        print("\n" + "=" * 70)
        print("INCIDENT RESPONSE (MULTI-PHASE)")
        print("=" * 70)
        print("--- Triage ---\n")
        print(result.get("triage_markdown", ""))
        print("\n--- Technical ---\n")
        print(result.get("technical_markdown", ""))
        print("\n--- Comms ---\n")
        print(result.get("comms_markdown", ""))
        print("\n--- Synthesis (raw) ---\n")
        print(result.get("synthesis_raw", ""))
        if result.get("structured"):
            print("\n--- Structured ---\n")
            print(result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Incident Response Agent")
    parser.add_argument(
        "--provider",
        default=os.getenv("INCIDENT_AGENT_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None)
    parser.add_argument("--temperature", type=float, default=0.25)
    parser.add_argument(
        "--run",
        action="store_true",
        help="Run 4-phase triage/technical/comms/synthesis pipeline",
    )
    parser.add_argument("--context", default="", help="Extra context or path to text file")
    parser.add_argument("--message", "-m", default=None)
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = IncidentResponseAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )

    if args.run:
        desc = args.message or (
            "Production API returning 503 for 15+ minutes. Dashboard shows DB connection pool exhausted. "
            "No deploy in last 4 hours."
        )
        ctx = args.context
        if ctx and os.path.isfile(os.path.expanduser(ctx)):
            with open(os.path.expanduser(ctx), "r", encoding="utf-8", errors="replace") as f:
                ctx = f.read()
        r = agent.run_full_response(
            incident_description=desc,
            extra_context=ctx or "",
            verbose=args.verbose,
        )
        agent.print_full_result(r)
        return

    msg = args.message or "What sections go in a blameless postmortem?"
    out = agent.chat(message=msg, verbose=args.verbose)
    print(out.get("content", ""))


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = IncidentResponseAgent(provider=os.getenv("INCIDENT_AGENT_PROVIDER", "openai"))
    r = agent.run_full_response(
        incident_description="Checkout errors spike; payment provider webhook delays.",
        verbose=True,
    )
    agent.print_full_result(r)


if __name__ == "__main__":
    main()
