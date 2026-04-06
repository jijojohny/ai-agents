# Newsletter Agent

Drafts **subject lines**, **preview text**, **sections**, and **markdown body** with compliance reminders. Optional JSON (`NewsletterReply`). Multi-provider LLM.

```bash
cd "newsletter agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Audience, topic, tone..."
```

Env: `NEWSLETTER_AGENT_PROVIDER`, `NEWSLETTER_AGENT_MODEL`.
