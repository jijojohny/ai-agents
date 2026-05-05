# Docker Compose Agent

Turns a **plain-language stack description** into a **Compose-oriented sketch** (services, networks, volumes, env/secrets notes, caveats). For iteration before you paste into `compose.yaml` and tune pins—**not** a substitute for ops review.

## Setup

```bash
cd "docker compose agent"
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env   # add OPENAI_API_KEY (or keys for other providers)
```

## Run

```bash
python main.py
python main.py -m "Describe your stack..."
```

Optional JSON: `ComposeSketchReply`. Env: `DOCKER_COMPOSE_AGENT_PROVIDER`, `DOCKER_COMPOSE_AGENT_MODEL`.
