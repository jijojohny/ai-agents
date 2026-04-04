# Stock Market Data & Analysis Agent

LangChain agent that **pulls public equity/index data** with [yfinance](https://github.com/ranaroussi/yfinance) (Yahoo Finance) and reasons over it with your choice of LLM (OpenAI, Anthropic, Gemini, Vertex).

## Tools

| Tool | Purpose |
|------|--------|
| `get_stock_quote` | Last price, recent closes, rough short-term change |
| `get_stock_history` | OHLCV over a period (`1mo`, `3mo`, `1y`, …), period return, highs/lows, last rows |
| `get_stock_profile` | Sector, market cap, PE, 52-week range, etc. (when `.info` returns data) |
| `get_stock_news` | Recent headlines/links for the symbol |

## Installation

```bash
cd "stock market agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
# Set OPENAI_API_KEY (or other provider) in .env
```

## CLI

```bash
python main.py -m "3mo history + quote for NVDA; note volatility, not advice." -v
python main.py
```

## Python

```python
from main import StockMarketAgent

agent = StockMarketAgent(provider="openai", model_name="gpt-4o-mini")
out = agent.chat("Fetch ^GSPC 6mo history and summarize the drawdowns.", verbose=True)
agent.print_result(out)
```

## Disclaimers

- **Not investment advice.** Educational and analytical only.
- Data can be **delayed**, **incomplete**, or **rate-limited**. Verify with your broker or exchange for trading decisions.
- Respect Yahoo/site terms of use; this agent uses the same endpoints as yfinance.

## Layout

```
stock market agent/
├── main.py
├── llm_factory.py
├── tools.py
├── schemas.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```
