# Freelance Scope Agent

Drafts **deliverables, milestones, assumptions, out-of-scope bullets**, and **high-level payment reminders** from a pasted brief. Useful as a **prep outline** before legal review—not a substitute for a lawyer.

## Setup

```bash
cd "freelance scope agent"
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env   # add OPENAI_API_KEY (or keys for other providers)
```

## Run

```bash
python main.py
python main.py -m "Your brief text..."
```

Optional JSON shape: `FreelanceScopeReply` (see `schemas.py`). Env: `FREELANCE_SCOPE_AGENT_PROVIDER`, `FREELANCE_SCOPE_AGENT_MODEL`.
