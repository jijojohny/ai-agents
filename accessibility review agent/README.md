# Accessibility Review Agent

Turns **descriptions of screens or flows** into **barrier-focused findings**, quick wins, and **testing suggestions** (keyboard, WCAG themes). Optional JSON (`A11yReviewReply` with `issues[]`). **Not** a formal audit—combine with automated tools and experts.

```bash
cd "accessibility review agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Describe your UI or paste structure..."
```

Env: `A11Y_REVIEW_AGENT_PROVIDER`, `A11Y_REVIEW_AGENT_MODEL`.
