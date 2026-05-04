# Regex & Log Parser Agent

Builds **regex / ripgrep-style** patterns for **log lines** with explanations, **test strings**, and **ReDoS / engine** caveats. Optional JSON (`LogParseReply`). Multi-provider LLM—**always validate** on real logs.

```bash
cd "regex log parser agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste sample lines + what to extract..." -v
```

Env: `REGEX_LOG_PARSER_AGENT_PROVIDER`, `REGEX_LOG_PARSER_AGENT_MODEL`.
