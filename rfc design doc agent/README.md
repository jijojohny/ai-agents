# RFC Design Doc Agent

Drafts **engineering RFCs / design docs** (problem, goals/non-goals, proposal, alternatives, risks, open questions). Optional JSON (`RfcDesignDocReply`). Multi-provider LLM.

```bash
cd "rfc design doc agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Problem + proposed approach..."
```

Env: `RFC_DESIGN_DOC_AGENT_PROVIDER`, `RFC_DESIGN_DOC_AGENT_MODEL`.
