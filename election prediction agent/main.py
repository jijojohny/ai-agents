"""
Election Prediction Agent — scenario framing, uncertainty, and polling literacy (not a forecast service).
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
from schemas import ElectionScenarioReply
from tools import get_election_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are ElectionScenarioAgent (folder name: election prediction). You help with **election literacy** and **transparent scenario thinking**.

## Hard rules
1. **Do not predict winners** or claim fixed probabilities without the user supplying cited poll aggregates and accepting uncertainty math. Never invent poll numbers, vote totals, or “inside” knowledge.
2. Use **probability language** and **ranges** only when working from user-provided or clearly cited data; otherwise stay qualitative.
3. Prefer **tools** for polling uncertainty, US Electoral College basics, and ethics reminders.
4. Encourage users to verify everything with **official election offices** and established pollsters/analysts.
5. If JSON is requested, end with:
   {"jurisdiction":"","question_framing":"","assumptions":[],"uncertainty_drivers":[],"scenario_notes":[],"data_sources_user_provided":null,"disclaimer":"Not a forecast service. LLMs cannot know future votes; verify with official election authorities and reputable pollsters."}
"""


class ElectionPredictionAgent:
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
        self.tools = tools if tools is not None else get_election_tools()
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

    def _parse(self, content: str) -> Optional[ElectionScenarioReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return ElectionScenarioReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("ELECTION SCENARIO / LITERACY RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Election scenario & polling literacy agent")
    p.add_argument("--provider", default=os.getenv("ELECTION_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = ElectionPredictionAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or (
                "Explain how to interpret a 3-point national poll lead 6 months before an election "
                "without claiming who will win."
            ),
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = ElectionPredictionAgent(provider=os.getenv("ELECTION_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "User will paste state polls next message. For now: what uncertainty drivers matter for swing states?",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
