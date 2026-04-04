"""
Stock Market Agent — fetches public market data via yfinance and analyzes with an LLM.
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
from schemas import StockAnalysisReply
from tools import get_stock_market_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are StockMarketAgent. You help users understand equities and indices using **live-fetched** data.

## Rules
1. **Always call tools** for prices, history, profile, or news. Never invent numbers, dates, or returns.
2. If a tool returns an error or empty data, say so and suggest checking the ticker, market hours, or rate limits.
3. Analysis must be **educational**, not personalized investment, tax, or legal advice. Say clearly: "Not investment advice."
4. Yahoo Finance data can be **delayed** or incomplete; mention uncertainty when relevant.
5. For comparisons (e.g. AAPL vs MSFT), fetch data for **each** symbol.
6. When the user wants structured output, end with JSON only (no markdown fences) matching:
   {"symbol":"...","headline":"...","summary":"...","key_metrics":[],"risk_factors":[],"disclaimer":"Not investment advice. Data may be delayed or incomplete.","data_sources_note":"..."}
"""


class StockMarketAgent:
    """LangChain agent: yfinance tools + multi-provider LLM."""

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
        self.tools = tools if tools is not None else get_stock_market_tools()
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def chat(self, message: str, verbose: bool = False) -> Dict[str, Any]:
        user_text = (message or "").strip()
        if verbose:
            print(f"Provider: {self.provider}")
        result = self.agent.invoke({"messages": [HumanMessage(content=user_text)]})
        messages = result.get("messages", [])
        content = ""
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None) or str(last)
        structured = self._try_parse(content)
        return {
            "message": user_text,
            "messages": messages,
            "content": content,
            "structured": structured,
        }

    def _try_parse(self, content: str) -> Optional[StockAnalysisReply]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content) or re.search(r"\{[\s\S]*\}", content)
            if m:
                return StockAnalysisReply(**json.loads(m.group()))
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("STOCK MARKET AGENT RESULT")
        print("=" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print(result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    p = argparse.ArgumentParser(description="Stock Market Data & Analysis Agent")
    p.add_argument("--provider", default=os.getenv("STOCK_MARKET_AGENT_PROVIDER", "openai"))
    p.add_argument("--model", default=None)
    p.add_argument("--temperature", type=float, default=0.25)
    p.add_argument("--message", "-m", default=None)
    p.add_argument("-v", "--verbose", action="store_true")
    args = p.parse_args()

    agent = StockMarketAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )
    msg = args.message or (
        "Fetch 3-month history and a quote for AAPL. Summarize trend and key risks (not advice)."
    )
    agent.print_result(agent.chat(msg, verbose=args.verbose))


def main() -> None:
    import sys

    if len(sys.argv) > 1:
        _cli()
        return
    agent = StockMarketAgent(provider=os.getenv("STOCK_MARKET_AGENT_PROVIDER", "openai"))
    agent.print_result(
        agent.chat(
            "Compare last month performance of SPY and QQQ using history tools. Not investment advice.",
            verbose=True,
        )
    )


if __name__ == "__main__":
    main()
