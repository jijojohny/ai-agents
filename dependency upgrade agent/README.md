# Dependency Upgrade Agent

Plans **dependency upgrades** (order, breaking-change watchlist, tests, rollback) from user-provided package/version context. Does **not invent** CVE/changelog facts. Optional JSON (`DependencyUpgradeReply`). Multi-provider LLM.

```bash
cd "dependency upgrade agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Ecosystem + packages + current/target versions..."
```

Env: `DEPENDENCY_UPGRADE_AGENT_PROVIDER`, `DEPENDENCY_UPGRADE_AGENT_MODEL`.
