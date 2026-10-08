# Error Message UX Agent

Rewrites raw/technical errors into **clear, safe, actionable** user-facing copy with recovery steps. Optional JSON (`ErrorMessageUxReply`). Multi-provider LLM.

```bash
cd "error message ux agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Raw error + UI context..."
```

Env: `ERROR_MESSAGE_UX_AGENT_PROVIDER`, `ERROR_MESSAGE_UX_AGENT_MODEL`.
