"""
Web Scraping Agent — fetch URL content via tools and reason with multiple LLM backends.

Supports: OpenAI, Anthropic (Claude), Google Gemini (API key), Google Vertex AI.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, SystemMessage

from llm_factory import build_chat_model
from schemas import ScrapeInsight
from tools import fetch_webpage_text_impl, get_scraping_tools

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

SYSTEM_PROMPT = """You are WebScrapingAgent, an assistant that extracts and summarizes information from websites.

## Rules
1. Use tools to fetch real page content. Do not invent page text.
2. If the user gives URL(s), call fetch_webpage_text for each important URL.
3. Use list_page_links when you need to discover subpages on the same site (docs, pricing, etc.).
4. Respect copyright and site terms; only access public URLs the user is allowed to scrape.
5. If a fetch fails, say what failed and suggest fixes (wrong URL, paywall, blocking).
6. Answer clearly: summary, key bullet points, and cite which URL each claim came from.
7. When the user wants structured output, end with a JSON object matching this shape:
   {"source_url": "...", "summary": "...", "key_points": ["..."], "tables_or_data_notes": null, "follow_up_urls": [], "confidence": "medium"}
"""


class WebScrapingAgent:
    """LangChain agent with fetch tools + pluggable chat model."""

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
        self.tools = tools if tools is not None else get_scraping_tools()
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
        )

    def run(
        self,
        query: str,
        urls: Optional[List[str]] = None,
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Run the agent on a natural-language query; optionally seed with URLs in the message.

        Args:
            query: What to extract or answer (e.g. "Summarize pricing from this page").
            urls: Optional list of URLs to include in the user message for context.
            verbose: Print the final assistant text.

        Returns:
            Dict with keys: query, urls, messages, content, structured (ScrapeInsight or None).
        """
        parts = [query.strip()]
        if urls:
            parts.append("URLs to use:\n" + "\n".join(urls))
        user_text = "\n\n".join(parts)

        if verbose:
            print(f"Provider: {self.provider}")
            print(f"Query: {query[:200]}...")

        result = self.agent.invoke({"messages": [HumanMessage(content=user_text)]})
        messages = result.get("messages", [])
        content = ""
        if messages:
            last = messages[-1]
            content = getattr(last, "content", None) or str(last)

        structured = self._try_parse_structured(content)

        out: Dict[str, Any] = {
            "query": query,
            "urls": urls or [],
            "messages": messages,
            "content": content,
            "structured": structured,
        }
        if verbose:
            print("\n--- Response ---\n")
            print(content[:8000] if len(content) > 8000 else content)
        return out

    def quick_extract(
        self,
        url: str,
        instruction: str = "Summarize the main content and list key facts.",
        verbose: bool = False,
    ) -> Dict[str, Any]:
        """
        Fetch one URL without the agent loop, then answer in one LLM call (faster for simple pages).

        Args:
            url: Page to fetch.
            instruction: What to extract.
            verbose: Print preview of fetched text length.

        Returns:
            Dict with url, raw_tool_preview, content, structured.
        """
        raw = fetch_webpage_text_impl(url, max_characters=20000)
        if verbose:
            print(f"Fetched chars (approx): {len(raw)}")

        user = (
            f"{instruction}\n\n"
            f"Below is extracted text from the page. Base your answer only on this text.\n\n"
            f"{raw}"
        )
        resp = self.llm.invoke(
            [
                SystemMessage(
                    content="You are a precise analyst. Only use the provided page text. "
                    "If information is missing, say so."
                ),
                HumanMessage(content=user),
            ]
        )
        text = getattr(resp, "content", None) or str(resp)
        structured = self._try_parse_structured(text)
        return {
            "url": url,
            "raw_tool_preview": raw[:500] + "..." if len(raw) > 500 else raw,
            "content": text,
            "structured": structured,
        }

    def _try_parse_structured(self, content: str) -> Optional[ScrapeInsight]:
        try:
            m = re.search(r"\{[\s\S]*\}\s*$", content)
            if not m:
                m = re.search(r"\{[\s\S]*\}", content)
            if m:
                data = json.loads(m.group())
                return ScrapeInsight(**data)
        except Exception:
            pass
        return None

    def print_result(self, result: Dict[str, Any]) -> None:
        print("\n" + "=" * 70)
        print("WEB SCRAPING AGENT RESULT")
        print("=" * 70)
        print(f"Query: {result.get('query', 'N/A')}")
        if result.get("urls"):
            print(f"URLs: {', '.join(result['urls'])}")
        print("-" * 70)
        print(result.get("content", ""))
        if result.get("structured"):
            print("-" * 70)
            print("Structured:", result["structured"].model_dump_json(indent=2))
        print("=" * 70 + "\n")


def _cli() -> None:
    parser = argparse.ArgumentParser(description="Web Scraping Agent (multi-provider LLM)")
    parser.add_argument(
        "--provider",
        default=os.getenv("WEB_SCRAPER_PROVIDER", "openai"),
        help="openai | anthropic | google | gemini | vertex",
    )
    parser.add_argument("--model", default=None, help="Model id (optional)")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--query", help="Natural language task")
    parser.add_argument(
        "--url",
        action="append",
        dest="urls",
        default=[],
        help="URL (repeatable)",
    )
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Single URL: fetch + one LLM call (no tool agent loop)",
    )
    parser.add_argument(
        "--instruction",
        default="Summarize the main content and list key facts.",
        help="Used with --quick",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    agent = WebScrapingAgent(
        provider=args.provider,
        model_name=args.model,
        temperature=args.temperature,
    )

    if args.quick:
        if not args.urls or len(args.urls) != 1:
            raise SystemExit("--quick requires exactly one --url")
        r = agent.quick_extract(args.urls[0], instruction=args.instruction, verbose=args.verbose)
        print("\n" + "=" * 70)
        print("QUICK EXTRACT")
        print("=" * 70)
        print(r.get("content", ""))
        return

    q = args.query or (
        "Fetch the given URL(s), summarize the content, and list key takeaways with source URLs."
    )
    r = agent.run(query=q, urls=args.urls or None, verbose=args.verbose)
    agent.print_result(r)


def main() -> None:
    """Demo when run without CLI args (uses example.com if no query)."""
    import sys

    if len(sys.argv) > 1:
        _cli()
        return

    agent = WebScrapingAgent(provider=os.getenv("WEB_SCRAPER_PROVIDER", "openai"))
    result = agent.run(
        query="What is this site? Summarize in 3 bullets.",
        urls=["https://example.com/"],
        verbose=True,
    )
    agent.print_result(result)


if __name__ == "__main__":
    main()
