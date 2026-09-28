# Job Description Writer Agent

Drafts **inclusive, structured job descriptions** (title options, summary, responsibilities, must/nice requirements, open questions). Optional JSON (`JobDescriptionReply`). Multi-provider LLM.

```bash
cd "job description writer agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Role, seniority, location/work model, stack..."
```

Env: `JOB_DESCRIPTION_WRITER_AGENT_PROVIDER`, `JOB_DESCRIPTION_WRITER_AGENT_MODEL`. Does **not** invent salary or benefits you did not provide.
