# Pull Request Review Agent

Produces **constructive PR feedback** from a **description**, **diff summary**, or pasted snippet: strengths, threaded-style **comments** (severity), **test gaps**, **security/privacy** notes, and a **merge recommendation**. Tools cover **review tone** and **severity rubric**. Optional JSON (`PRReviewReply`). Multi-provider LLM.

```bash
cd "pull request review agent"
pip install -r requirements.txt && cp .env-example .env
python main.py -m "Paste or describe the change..." -v
```

Env: `PR_REVIEW_AGENT_PROVIDER`, `PR_REVIEW_AGENT_MODEL`. This does **not** clone repos or run tests—pair with CI for real merges.
