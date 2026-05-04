# Open Source Issue Triage Agent

Drafts **first maintainer replies**, **label ideas**, and a **triage checklist** from pasted issue text—plus **security disclosure** reminders. Optional JSON (`OSSTriageReply`). Multi-provider LLM; adapt to your project’s `CONTRIBUTING.md` and CoC.

```bash
cd "open source triage agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste issue title + body..." -v
```

Env: `OSS_TRIAGE_AGENT_PROVIDER`, `OSS_TRIAGE_AGENT_MODEL`.
