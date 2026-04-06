# YouTube Script Agent

Plans **titles, hooks, outlines, script beats, CTAs**, and short **description** snippets with optional structured JSON (`YouTubeScriptReply`). Multi-provider LLM.

```bash
cd "youtube script agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Topic, length, audience..."
```

Env: `YOUTUBE_SCRIPT_AGENT_PROVIDER`, `YOUTUBE_SCRIPT_AGENT_MODEL`.
