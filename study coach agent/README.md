# Study Coach Agent

Turns **notes or topics** into **flashcards**, **practice questions**, and light **schedule hints**. Multi-provider LLM; optional structured JSON (`StudyPackReply`).

```bash
cd "study coach agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste notes or ask for cards on a topic..."
```

Environment: `STUDY_COACH_AGENT_PROVIDER`, `STUDY_COACH_AGENT_MODEL`.
