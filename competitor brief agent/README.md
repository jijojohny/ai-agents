# Competitor Brief Agent

Turns **user-provided competitor notes** into a structured brief (positioning, strengths/weaknesses, differentiation, research next steps). **Does not invent** ARR/market share. Optional JSON (`CompetitorBriefReply`). Multi-provider LLM.

```bash
cd "competitor brief agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Your product + competitor notes..."
```

Env: `COMPETITOR_BRIEF_AGENT_PROVIDER`, `COMPETITOR_BRIEF_AGENT_MODEL`. Verify claims with public sources.
