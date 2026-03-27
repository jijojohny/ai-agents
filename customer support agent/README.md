# Customer Support Agent

A LangChain customer support agent that drafts clear and empathetic responses, classifies incoming issues, and generates a practical refund-intake checklist when needed.

## Installation

```bash
cd "customer support agent"
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env-example .env
# Add keys for your chosen provider
```

## Usage (Python)

```python
from main import CustomerSupportAgent

agent = CustomerSupportAgent(provider="openai", model_name="gpt-4o-mini")
result = agent.chat(
    message="I was charged twice for one order. Please help.",
    verbose=True,
)
agent.print_result(result)
```

## CLI

```bash
python main.py -m "My order is damaged and I want a refund."
python main.py --provider anthropic -m "Where is my package?"
python main.py
```

## Project layout

```
customer support agent/
├── main.py
├── llm_factory.py
├── tools.py
├── schemas.py
├── example.py
├── requirements.txt
├── .env-example
└── README.md
```
