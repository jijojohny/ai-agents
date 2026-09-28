import os
from dotenv import load_dotenv
from main import SEOContentBriefAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = SEOContentBriefAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Guide: 'how to migrate from Heroku to AWS ECS'. Intent informational. JSON at end.",
            verbose=True,
        )
    )
