# Election Result Analysis Agent (AGI-style multi-phase)

This agent runs **five sequential specialist LLM phases** (intake → descriptive analysis → institutional context → media literacy → structured JSON). **“AGI-style”** means **multi-specialist orchestration**, not artificial general intelligence.

## What it is for

- **After** votes are reported: structure **user-pasted** or **user-cited** official/unofficial tallies
- Describe margins, turnout, and shifts **only when you supply comparable numbers**
- High-level **certification / recount / provisional** concepts (not legal advice)
- **Headline vs evidence** discipline

## What it is not

- **No live election-night scraping** of results feeds
- **No invented statistics** or winners not in your message
- **Not legal advice** — verify with election officials and counsel

## Installation

```bash
cd "election result analysis agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## Full pipeline (recommended)

```bash
python main.py --pipeline -m "Paste results with source + date + office..." -v
python main.py --pipeline -m "..." --notes ./extra.txt
```

## Chat mode (tools only)

```bash
python main.py -m "How should I cite county canvass numbers in a memo?"
```

## Output schema

Final phase parses **`ElectionResultAnalysisReport`** when the model emits valid JSON.

## Environment

| Variable | Meaning |
|----------|---------|
| `ELECTION_RESULT_AGENT_PROVIDER` | `openai` (default), `anthropic`, `google`, `vertex` |
| `ELECTION_RESULT_AGENT_MODEL` | Optional default model id |
