# Release Notes Agent

Turns **commit/PR bullets** into **customer-facing release notes** (highlights, features, fixes, breaking changes, markdown body). Does not invent changes. Optional JSON (`ReleaseNotesReply`). Multi-provider LLM.

```bash
cd "release notes agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste version + commits/PRs..."
```

Env: `RELEASE_NOTES_AGENT_PROVIDER`, `RELEASE_NOTES_AGENT_MODEL`.
