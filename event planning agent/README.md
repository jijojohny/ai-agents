# Event Planning Agent

Builds **run-of-show lines**, **pre/during/post phases**, **logistics checklists**, and **risk notes** from a short brief (format, audience, duration, venue or virtual). Planning aid only—confirm permits, budgets, and contracts locally.

## Setup

```bash
cd "event planning agent"
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env   # add OPENAI_API_KEY (or keys for other providers)
```

## Run

```bash
python main.py
python main.py -m "Your event constraints..."
```

Optional JSON: `EventPlanReply`. Env: `EVENT_PLANNING_AGENT_PROVIDER`, `EVENT_PLANNING_AGENT_MODEL`.
