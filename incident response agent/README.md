# Incident Response Agent (Advanced)

**Four-phase** incident workflow: **Triage** → **Technical** (contain / investigate / recover) → **Comms** (internal + optional external) → **Synthesis** as structured JSON (`IncidentResponseReport`). Includes a **chat** mode with playbook tools.

## Why this is “advanced”

- **Sequential specialist prompts** with each phase fed prior outputs (like a mini incident bridge).
- Final phase targets a **validated schema** for handoff to tickets, status pages, or docs.

## Installation

```bash
cd "incident response agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## Full pipeline (CLI)

```bash
python main.py --run -m "Describe the incident..." -v
python main.py --run -m "..." --context ./facts.txt
```

## Chat (tools)

```bash
python main.py -m "Show severity cheatsheet and postmortem outline."
```

## Python API

```python
from main import IncidentResponseAgent

agent = IncidentResponseAgent(provider="openai")
out = agent.run_full_response(
    incident_description="Kafka lag growing; consumers falling behind.",
    extra_context="No recent config change.",
    verbose=True,
)
agent.print_full_result(out)
```

## Disclaimer

This is **decision support only**. It does not access your stack, logs, or paging systems. Validate all actions against your runbooks and on-call policy.

## Layout

```
incident response agent/
├── main.py
├── orchestrator.py
├── llm_factory.py
├── schemas.py
├── tools.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```
