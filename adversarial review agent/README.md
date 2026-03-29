# Adversarial Review Agent (Advanced)

Multi-phase **decision review**: **Analyst** (neutral decomposition) → **Red Team** (stress test) → **Blue Team** (mitigations) → **Chair** (structured JSON verdict). Also includes a lightweight **chat** mode with rubric tools.

## Why this is “advanced”

- **Four sequential LLM phases** with accumulated context (not a single prompt).
- Final phase returns a **Pydantic-validated** `AdversarialReviewReport` when the model emits valid JSON.

## Installation

```bash
cd "adversarial review agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
```

## Deep pipeline (CLI)

```bash
python main.py --deep -m "Proposal text..." -v
python main.py --deep -m "..." --context ./notes.txt
```

## Chat mode (tools only)

```bash
python main.py -m "Show me the risk review dimensions rubric."
```

## Python API

```python
from main import AdversarialReviewAgent

agent = AdversarialReviewAgent(provider="openai", model_name="gpt-4o-mini")
report = agent.run_deep_review(
    proposal="Ship feature X with default-on data sharing.",
    extra_context="EU users ~40%.",
    verbose=True,
)
agent.print_deep_result(report)
# report["structured"] is AdversarialReviewReport | None
```

## Layout

```
adversarial review agent/
├── main.py
├── orchestrator.py
├── llm_factory.py
├── schemas.py
├── tools.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```

## Safety

Red-team prompts are for **legitimate** risk analysis (product, security, compliance). Do not use outputs to harass, target individuals, or plan illegal activity.
