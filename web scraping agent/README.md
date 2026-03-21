# Web Scraping Agent

LangChain agent that **fetches real web pages** (via HTTP) and answers questions using a **pluggable LLM**: OpenAI, Anthropic (Claude), Google Gemini (API key), or **Google Vertex AI**.

## Features

- **Multi-provider LLMs** — switch with `provider=` or `WEB_SCRAPER_PROVIDER` (no OpenAI lock-in)
- **Tools**: `fetch_webpage_text` (HTML → clean text), `list_page_links` (discover same-site links)
- **Agent mode** — model decides when to call tools (`create_agent`)
- **Quick mode** — one fetch + one LLM call (`quick_extract`) for simple pages
- **Optional structured output** — Pydantic `ScrapeInsight` when the model returns JSON

## Installation

```bash
cd "web scraping agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt --index-url https://pypi.org/simple/
cp .env-example .env
# Add keys for the provider(s) you use
```

You only need **one** LLM backend installed/configured. Optional packages:

| Provider | Env vars | Package |
|----------|-----------|---------|
| OpenAI | `OPENAI_API_KEY` | `langchain-openai` |
| Anthropic | `ANTHROPIC_API_KEY` | `langchain-anthropic` |
| Google Gemini | `GOOGLE_API_KEY` or `GEMINI_API_KEY` | `langchain-google-genai` |
| Vertex AI | `GOOGLE_CLOUD_PROJECT`, ADC or `GOOGLE_APPLICATION_CREDENTIALS` | `langchain-google-vertexai` |

Vertex also uses `GOOGLE_CLOUD_LOCATION` (default `us-central1` if unset).

## Usage (Python)

```python
from main import WebScrapingAgent

# OpenAI (default)
agent = WebScrapingAgent(provider="openai", model_name="gpt-4o-mini")
result = agent.run(
    query="Summarize the main message of the page in 3 bullets.",
    urls=["https://example.com/"],
    verbose=True,
)
agent.print_result(result)
```

```python
# Claude
agent = WebScrapingAgent(provider="anthropic", model_name="claude-3-5-sonnet-20241022")

# Gemini (API key)
agent = WebScrapingAgent(provider="google", model_name="gemini-2.0-flash")

# Vertex AI (GCP project + credentials)
agent = WebScrapingAgent(provider="vertex", model_name="gemini-2.0-flash")
```

```python
# Fast path: no agent loop
agent = WebScrapingAgent(provider="openai")
out = agent.quick_extract("https://example.com/", instruction="One short paragraph.")
print(out["content"])
```

## CLI

```bash
# Agent mode with URLs
python main.py --provider openai --url https://example.com/ --query "Summarize this page."

# Quick mode (single URL)
python main.py --provider anthropic --quick --url https://example.com/ --instruction "List key facts."

# Default demo (no args): scrapes example.com with provider from env or openai
python main.py
```

Pass `--verbose` / `-v` for longer console output.

## Ethics & limits

- Use only sites you are allowed to access; respect **robots.txt**, **terms of service**, and **rate limits**.
- Many sites are **JavaScript-heavy**; this agent uses **HTTP + HTML parsing** (no browser). For SPAs you may need a different fetch strategy.
- Do not use for paywalled or private content without permission.

## Project layout

```
web scraping agent/
├── main.py           # WebScrapingAgent + CLI
├── llm_factory.py  # OpenAI / Anthropic / Gemini / Vertex constructors
├── tools.py          # fetch_webpage_text, list_page_links
├── schemas.py        # ScrapeInsight
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```

## License

MIT (same spirit as other agents in this repo).
