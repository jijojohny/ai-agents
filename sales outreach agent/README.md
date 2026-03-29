# Sales Outreach Agent

Drafts **email** and **LinkedIn-style** outbound messages: hooks, body, CTA, follow-up cadence ideas, and “verify before send” research prompts. Multi-provider LLM; optional JSON via `OutreachReply`.

```bash
cd "sales outreach agent"
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
python main.py -m "Your ICP, offer, and channel..."
```

Environment: `SALES_OUTREACH_AGENT_PROVIDER`, `SALES_OUTREACH_AGENT_MODEL`.
