# DevOps Pipeline Agent

Sketches **CI/CD** flows (defaults to **GitHub Actions**): triggers, jobs, **secrets/OIDC** notes, caching, and a **commented YAML skeleton**. Optional JSON (`PipelineSketchReply`). Multi-provider LLM—**validate YAML** against official docs before merge.

```bash
cd "devops pipeline agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Stack, hosting, deploy target..." -v
```

Env: `DEVOPS_PIPELINE_AGENT_PROVIDER`, `DEVOPS_PIPELINE_AGENT_MODEL`.
