# Podcast Show Notes Agent

Builds **episode titles**, **hook**, **chapters** (timestamp placeholders), **takeaways**, **links**, and **markdown show notes** from your outline or transcript snippets. Multi-provider LLM.

```bash
cd "podcast show notes agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste outline or transcript..." -v
```

Env: `PODCAST_SHOW_NOTES_AGENT_PROVIDER`, `PODCAST_SHOW_NOTES_AGENT_MODEL`.
