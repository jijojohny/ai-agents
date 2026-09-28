# Database Schema Design Agent

Sketches **relational data models** (tables, keys, indexes, constraints, optional DDL) from product requirements. Optional JSON (`DatabaseSchemaDesignReply`). Multi-provider LLM.

```bash
cd "database schema design agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Dialect + domain requirements..."
```

Env: `DATABASE_SCHEMA_DESIGN_AGENT_PROVIDER`, `DATABASE_SCHEMA_DESIGN_AGENT_MODEL`. Review migrations carefully before applying to production.
