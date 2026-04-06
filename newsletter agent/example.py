import os
from dotenv import load_dotenv
from main import NewsletterAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = NewsletterAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(agent.chat("SaaS changelog digest for power users.", verbose=True))
