"""
Examples: Web Scraping Agent with different LLM providers.

Set the matching API key in .env and install the optional package for that provider.
"""
import os

from dotenv import load_dotenv

from main import WebScrapingAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


def example_openai() -> None:
    agent = WebScrapingAgent(provider="openai", model_name="gpt-4o-mini")
    r = agent.run(
        query="Summarize the page and mention the domain purpose.",
        urls=["https://example.com/"],
        verbose=True,
    )
    agent.print_result(r)


def example_anthropic() -> None:
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Skip anthropic example: ANTHROPIC_API_KEY not set")
        return
    agent = WebScrapingAgent(provider="anthropic")
    r = agent.run(
        query="Extract any visible headings or main message from the page text.",
        urls=["https://example.com/"],
    )
    agent.print_result(r)


def example_google_gemini() -> None:
    if not (os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")):
        print("Skip google example: GOOGLE_API_KEY / GEMINI_API_KEY not set")
        return
    agent = WebScrapingAgent(provider="google", model_name="gemini-2.0-flash")
    r = agent.quick_extract("https://example.com/", instruction="One paragraph summary only.")
    print(r.get("content", ""))


def example_vertex() -> None:
    if not (
        os.getenv("GOOGLE_CLOUD_PROJECT")
        or os.getenv("GCP_PROJECT")
        or os.getenv("VERTEX_PROJECT")
    ):
        print("Skip vertex example: set GOOGLE_CLOUD_PROJECT (or GCP_PROJECT / VERTEX_PROJECT)")
        return
    agent = WebScrapingAgent(provider="vertex")
    r = agent.run(query="What is on this page?", urls=["https://example.com/"])
    agent.print_result(r)


if __name__ == "__main__":
    print("Running OpenAI example (set OPENAI_API_KEY)...")
    example_openai()
    # example_anthropic()
    # example_google_gemini()
    # example_vertex()
