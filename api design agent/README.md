# API Design Agent

Sketches **REST-style JSON APIs** from product requirements: **resources**, **endpoints**, **auth/security**, **errors & pagination**, **versioning**, and **open questions**. Tools cover **HTTP status** usage and **idempotency**. Optional structured JSON (`ApiDesignReply`). Multi-provider LLM.

```bash
cd "api design agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Describe features, clients, and constraints..."
```

Env: `API_DESIGN_AGENT_PROVIDER`, `API_DESIGN_AGENT_MODEL`. Refine with your API standards and OpenAPI/GraphQL choices.
