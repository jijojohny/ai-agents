# Bug Report Agent

A LangChain agent that converts vague problem descriptions into **structured bug reports**: title, summary, repro steps, expected vs actual, environment notes, rough severity hints, and suggested labels. Useful before filing Jira, GitHub Issues, or Linear tickets.

## Installation

```bash
cd "bug report agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## Usage (Python)

```python
from main import BugReportAgent

agent = BugReportAgent(provider="openai", model_name="gpt-4o-mini")
result = agent.chat(
    message="Login spins forever on Safari; fine on Firefox. No errors in console.",
    verbose=True,
)
agent.print_result(result)
```

## CLI

```bash
python main.py -m "Export CSV is empty when date range includes today."
python main.py
```

## Environment

| Variable | Meaning |
|----------|---------|
| `BUG_REPORT_AGENT_PROVIDER` | `openai` (default), `anthropic`, `google`, `vertex` |
| `BUG_REPORT_AGENT_MODEL` | Optional default model id |

## Project layout

```
bug report agent/
├── main.py
├── llm_factory.py
├── tools.py
├── schemas.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```
