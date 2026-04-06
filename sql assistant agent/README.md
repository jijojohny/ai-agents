# SQL Assistant Agent

Turns **natural language + schema hints** into **read-only** SQL (`SELECT` / `WITH`), with assumptions and **injection-safety** notes. Optional JSON (`SQLAssistantReply`). Multi-provider LLM.

```bash
cd "sql assistant agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Dialect, tables/columns, question..."
```

Env: `SQL_ASSISTANT_AGENT_PROVIDER`, `SQL_ASSISTANT_AGENT_MODEL`. **Review** generated SQL on non-production data before production use.
