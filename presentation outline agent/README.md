# Presentation Outline Agent

Produces **deck titles**, **audience/goal**, **storyline beats**, a **one-line-per-slide** outline, **speaker-note hints**, and a **closing CTA** from topic and duration. Tools for **pyramid-style** slides and **timing**. Optional JSON (`DeckOutlineReply`). Multi-provider LLM.

```bash
cd "presentation outline agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Topic, length, audience..." -v
```

Env: `PRESENTATION_OUTLINE_AGENT_PROVIDER`, `PRESENTATION_OUTLINE_AGENT_MODEL`.
