"""
YouTube Script Agent — titles, hooks, outlines, and script beats.
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
from schemas import YouTubeScriptReply
from tools import get_youtube_script_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are YouTubeScriptAgent. You help creators plan engaging, honest videos.

## Rules
1. Match niche, audience level, and video length the user states.
2. No clickbait that misrepresents content; no harmful stunts or illegal instructions.
3. Use tools for retention/hook references when useful.
4. If JSON is requested, end with:
   {"title_options":[],"hook":"","outline":[],"script_beats":[],"cta":"","description_snippet":"","retention_tips":[]}
"""


class YouTubeScriptAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.65,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = provider.strip().lower()
        self.llm = build_chat_model(
            provider=self.provider,
            model_name=model_name,
            temperature=temperature,
        )
        self.tools = tools if tools is not None else get_youtube_script_tools()
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

    def _parse(self, content: str) -> Optional[YouTubeScriptReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return YouTubeScriptReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, r: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("YOUTUBE SCRIPT RESULT")
        print("=" * 70)
        print(r.get("content", ""))
        if r.get("structured"):
            print("-" * 70)
            print(r["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="YouTube Script Agent")
    p.add_argument("--provider", default=os.getenv("YOUTUBE_SCRIPT_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.65)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()
    agent = YouTubeScriptAgent(args.provider, args.model, args.temperature)
    agent.print_result(
        agent.chat(
            args.message or "10-min video: Python asyncio for beginners. Hook + outline + CTA.",
            verbose=args.verbose,
        )
    )


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = YouTubeScriptAgent(provider=os.getenv("YOUTUBE_SCRIPT_AGENT_PROVIDER", "openai"))
    agent.print_result(agent.chat("Tutorial: Docker multi-stage builds for Node.", verbose=True))


if __name__ == "__main__":
    main()
