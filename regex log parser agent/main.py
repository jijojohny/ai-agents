"""Regex & Log Parser Agent — patterns and explanations for log lines."""
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
from schemas import LogParseReply
from tools import get_regex_log_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are RegexLogParserAgent. Help users write regex or ripgrep patterns for log parsing.

Rules: explain each capturing group; warn about catastrophic backtracking; do not claim pattern is correct without test cases.
If JSON requested, end with:
{"intent_summary":"","suggested_pattern":"","pattern_explanation":"","test_strings":[],"pitfalls":[]}
"""


class RegexLogParserAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.2,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_regex_log_tools()
        self.agent = create_agent(model=self.llm, tools=self.tools, system_prompt=SYS)

    def chat(self, message: str, verbose: bool = False) -> Dict[str, Any]:
        t = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        out = self.agent.invoke({"messages": [HumanMessage(content=t)]})
        msgs = out.get("messages", [])
        c = getattr(msgs[-1], "content", None) or str(msgs[-1]) if msgs else ""
        st = None
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", c) or re.search(r"\{[\s\S]*\}", c)
            if m:
                st = LogParseReply(**json.loads(m.group()))
        except Exception:
            pass
        return {"message": t, "messages": msgs, "content": c, "structured": st}

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70 + "\n" + r.get("content", "") + "\n")
        if r.get("structured"):
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def main() -> None:
    import sys

    if len(sys.argv) <= 1:
        ag = RegexLogParserAgent(provider=os.getenv("REGEX_LOG_PARSER_AGENT_PROVIDER", "openai"))
        ag.print_result(
            ag.chat(
                "Parse nginx lines: IP - - [timestamp] \"METHOD path HTTP/1.1\" status bytes. Sample line in message.",
                verbose=True,
            )
        )
        return
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("REGEX_LOG_PARSER_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.2)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    ag = RegexLogParserAgent(a.provider, a.model, a.temperature)
    ag.print_result(ag.chat(a.message or "Extract request_id=UUID from JSON log lines.", verbose=a.verbose))


if __name__ == "__main__":
    main()
