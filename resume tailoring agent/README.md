# Resume Tailoring Agent

Aligns **resume bullets and summary** with a **job description** using **honesty-first** rules: no invented employers, dates, or metrics—use placeholders or questions when data is missing. Tools cover **STAR-style bullets** and **ATS readability** tips. Optional JSON (`ResumeTailorReply`). Multi-provider LLM.

```bash
cd "resume tailoring agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste job description + your experience bullets..." -v
```

Env: `RESUME_TAILOR_AGENT_PROVIDER`, `RESUME_TAILOR_AGENT_MODEL`. Complements **Interview Prep Agent**; does not replace human proofreading.
