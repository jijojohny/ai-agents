# Grant Proposal Agent

Builds **grant / RFP outlines**: funder fit, problem, objectives, methods, outcomes/metrics, timeline, **budget categories** (no invented dollars), risks. Tools for **RFP alignment** and **budget ethics**. Optional JSON (`GrantOutlineReply`). Multi-provider LLM—**not** legal or institutional approval.

```bash
cd "grant proposal agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste RFP goals + your project facts..." -v
```

Env: `GRANT_PROPOSAL_AGENT_PROVIDER`, `GRANT_PROPOSAL_AGENT_MODEL`.
