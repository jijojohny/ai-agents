# SEO Content Brief Agent

Builds **SEO content briefs** (keywords, intent, titles, meta, H2 outline, PAA-style questions) **without inventing** volume/rankings. Optional JSON (`SEOContentBriefReply`). Multi-provider LLM.

```bash
cd "seo content brief agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Topic, primary keyword, audience..."
```

Env: `SEO_CONTENT_BRIEF_AGENT_PROVIDER`, `SEO_CONTENT_BRIEF_AGENT_MODEL`. Verify metrics in Search Console / keyword tools.
