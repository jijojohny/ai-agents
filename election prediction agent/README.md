# Election Prediction Agent (Scenario & Literacy)

This agent is **not** a real-time forecast engine and **does not fetch live polls**. It supports:

- **Polling literacy** (margin of error, likely-voter models, why snapshots ≠ outcomes)
- **Transparent scenario framing** when *you* paste or cite numbers
- **US Electoral College** high-level reminders (civic education)
- **Ethics** checklist for talking about estimates responsibly

The LLM **must not invent** poll margins or claim certain winners. Use official results and professional aggregators for decisions that matter.

## Installation

```bash
cd "election prediction agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## CLI

```bash
python main.py -m "Your question; paste any numbers you want analyzed with citations." -v
python main.py
```

## Environment

- `ELECTION_AGENT_PROVIDER` — `openai` (default), `anthropic`, `google`, `vertex`
- `ELECTION_AGENT_MODEL` — optional default model id

## Layout

```
election prediction agent/
├── main.py
├── llm_factory.py
├── tools.py
├── schemas.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```

## Legal / civic note

Election laws, disclosure rules, and platform policies vary by country and jurisdiction. This tool is for **education and drafting help** only.
