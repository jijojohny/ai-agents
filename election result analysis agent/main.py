"""
Election Result Analysis Agent — multi-phase (AGI-style) post-election analysis.

Orchestrates specialist passes over **user-provided or cited** results; does not fetch live tallies.
"""
from __future__ import annotations

import argparse
import os
from typing import Any, List, Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from llm_factory import build_chat_model
from orchestrator import run_election_result_pipeline
from tools import get_election_result_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

CHAT = """You support **post-election** analysis literacy. Use tools for citation, recount concepts, and headline discipline.
For the full five-phase specialist pipeline, run the CLI with --pipeline. Never invent vote totals."""


class ElectionResultAnalysisAgent:
    """
    AGI-style = multiple sequential specialist LLM phases + JSON synthesis (not literal AGI).
    """

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
        self.tools = tools if tools is not None else get_election_result_tools()
        self.agent = create_agent(model=self.llm, tools=self.tools, system_prompt=CHAT)

    def chat(self, message: str, verbose: bool = False) -> dict:
        t = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        out = self.agent.invoke({"messages": [HumanMessage(content=t)]})
        msgs = out.get("messages", [])
        c = getattr(msgs[-1], "content", None) or str(msgs[-1]) if msgs else ""
        return {"message": t, "messages": msgs, "content": c}

    def run_pipeline(
        self,
        results_and_context: str,
        extra_notes: str = "",
        verbose: bool = False,
    ) -> dict:
        return run_election_result_pipeline(
            self.llm,
            results_and_context=results_and_context,
            extra_notes=extra_notes,
            verbose=verbose,
        )

    def print_pipeline(self, r: dict) -> None:
        print("\n" + "=" * 70)
        print("ELECTION RESULT ANALYSIS (5-phase)")
        print("=" * 70)
        for k in (
            "phase1_intake",
            "phase2_descriptive",
            "phase3_institutional",
            "phase4_media_literacy",
        ):
            print(f"\n--- {k} ---\n")
            print(r.get(k, ""))
        print("\n--- phase5_raw ---\n")
        print(r.get("phase5_raw", ""))
        if r.get("structured"):
            print("\n--- structured ---\n")
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Election Result Analysis Agent (multi-phase)")
    p.add_argument("--provider", default=os.getenv("ELECTION_RESULT_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument(
        "--pipeline",
        action="store_true",
        help="Run 5-phase intake→description→institutions→media→JSON",
    )
    p.add_argument("--notes", default="", help="Extra context or path to text file")
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    agent = ElectionResultAnalysisAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )

    if args.pipeline:
        text = args.message or (
            "Example (replace with real cited data): City Dogcatcher race, Ward 4. "
            "Unofficial 2025-11-05 21:00 from city site: Candidate A 1,240 (51.2%), B 1,180 (48.8%). "
            "92% precincts reporting."
        )
        notes = args.notes
        if notes and os.path.isfile(os.path.expanduser(notes)):
            with open(os.path.expanduser(notes), "r", encoding="utf-8", errors="replace") as f:
                notes = f.read()
        out = agent.run_pipeline(
            results_and_context=text,
            extra_notes=notes or "",
            verbose=args.verbose,
        )
        agent.print_pipeline(out)
        return

    print(
        agent.chat(
            args.message or "What should I verify before trusting a county results PDF?",
            verbose=args.verbose,
        ).get("content", "")
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = ElectionResultAnalysisAgent(provider=os.getenv("ELECTION_RESULT_AGENT_PROVIDER", "openai"))
    agent.print_pipeline(
        agent.run_pipeline(
            results_and_context=(
                "Hypothetical drill: State X Governor. Certified final: Candidate P 2,100,000 (49.9%), "
                "Q 2,105,000 (50.1%). Source: state SOS certified canvass 2024-12-01."
            ),
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
