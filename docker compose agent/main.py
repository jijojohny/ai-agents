"""Docker Compose Agent — sketch compose layouts from described services."""
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
from schemas import ComposeSketchReply
from tools import get_compose_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYS = """You are DockerComposeAgent. From a description of apps/databases/cache/reverse-proxy needs, sketch a **reasonable Compose-oriented layout**.

Prefer YAML-shaped snippets or clearly labeled pseudo-blocks. Pin images where sensible; say when versions are placeholders.

If JSON requested, end with:
{"summary":"","services":[],"networks":[],"volumes":[],"env_and_secrets_notes":[],"caveats":[]}
"""


class DockerComposeAgent:
    def __init__(
        self,
        provider: str = "openai",
        model_name: Optional[str] = None,
        temperature: float = 0.4,
        tools: Optional[List[Any]] = None,
    ):
        self.provider = (provider or "openai").strip().lower()
        self.llm = build_chat_model(self.provider, model_name, temperature)
        self.tools = tools or get_compose_tools()
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
                st = ComposeSketchReply(**json.loads(m.group()))
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
        ag = DockerComposeAgent(provider=os.getenv("DOCKER_COMPOSE_AGENT_PROVIDER", "openai"))
        ag.print_result(
            ag.chat(
                "Local dev: FastAPI + Postgres 16 + Redis + nginx in front, one internal network.",
                verbose=True,
            )
        )
        return
    p = argparse.ArgumentParser()
    p.add_argument("--provider", default=os.getenv("DOCKER_COMPOSE_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.4)
    p.add_argument("-m", "--message", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    a = p.parse_args()
    ag = DockerComposeAgent(a.provider, a.model, a.temperature)
    ag.print_result(
        ag.chat(a.message or "Single-node WordPress + mysql + phpMyAdmin for staging.", verbose=a.verbose)
    )


if __name__ == "__main__":
    main()
