# Meeting Notes Agent

A LangChain agent that transforms rough meeting notes into clear summaries, decisions, action items, and risk flags.

## Installation

```bash
cd "meeting notes agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## Usage (Python)

```python
from main import MeetingNotesAgent

agent = MeetingNotesAgent(provider="openai", model_name="gpt-4o-mini")
result = agent.chat(
    message="Summarize: Decision to delay launch. Priya owns QA checklist by Friday.",
    verbose=True,
)
agent.print_result(result)
```

## CLI

```bash
python main.py -m "Decision: postpone release. Action: Sam to notify stakeholders."
python main.py
```

## Project layout

```
meeting notes agent/
├── main.py
├── llm_factory.py
├── tools.py
├── schemas.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```
