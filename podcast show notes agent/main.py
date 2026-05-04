"""Podcast Show Notes Agent — titles, chapters, summary, links from outline or transcript."""
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
from schemas import PodcastNotesReply
from tools import get_podcast_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are PodcastShowNotesAgent. Create publishable show notes from the user's outline or transcript excerpts.

Rules: do not invent quotes or guests not mentioned; use [timestamp] placeholders if times unknown.
If JSON requested, end with:
{"episode_title_options":[],"one_line_hook":"","summary":"","chapters":[],"key_takeaways":[],"links_and_resources":[],"show_notes_body_markdown":""}
"""


class PodcastShowNotesAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.5,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_podcast_tools()
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
                st = PodcastNotesReply(**json.loads(m.group()))
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
        agent = PodcastShowNotesAgent(provider=os.getenv("PODCAST_SHOW_NOTES_AGENT_PROVIDER", "openai"))
        agent.print_result(
            agent.chat(
                "Episode: interviewing a DB reliability engineer about failover drills. 45 min. No transcript yet.",
                verbose=True,
            )
        )
        return

    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("PODCAST_SHOW_NOTES_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.5)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = PodcastShowNotesAgent(args.provider, args.model, args.temperature)
    msg = args.message or "Episode: climate tech solo 20 min."
    agent.print_result(agent.chat(msg, verbose=args.verbose))


if __name__ == "__main__":
    main()
