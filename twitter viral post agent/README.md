# Twitter / X Viral Post Agent

A LangChain agent that drafts **X (Twitter)** posts optimized for strong hooks, clarity, and shareability: single posts, alternates, optional thread outlines, and light posting tips. It includes tools to check length against a **280-character** budget (standard accounts) and to list common high-performing **formats** (to use ethically).

## Installation

```bash
cd "twitter viral post agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## Usage (Python)

```python
from main import TwitterViralPostAgent

agent = TwitterViralPostAgent(provider="openai", model_name="gpt-4o-mini", temperature=0.8)
result = agent.chat(
    message="Write a viral-style post about why 'learn in public' beats silent grinding.",
    verbose=True,
)
agent.print_result(result)
```

## CLI

```bash
python main.py -m "Thread opener + outline: 5 mistakes new devs make with APIs."
python main.py
```

## Environment

| Variable | Meaning |
|----------|---------|
| `TWITTER_VIRAL_AGENT_PROVIDER` | `openai` (default), `anthropic`, `google`, `vertex` |
| `TWITTER_VIRAL_AGENT_MODEL` | Optional default model id |

## Project layout

```
twitter viral post agent/
├── main.py
├── llm_factory.py
├── tools.py
├── schemas.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```

## Note

This agent generates **text only**. Posting to X requires your own app credentials and compliance with [X’s rules](https://help.x.com/en/rules-and-policies/twitter-rules) and applicable law.
