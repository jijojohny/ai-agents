import os
from dotenv import load_dotenv
from main import YouTubeScriptAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = YouTubeScriptAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat("8 min: how I use Obsidian for dev notes.", verbose=True)
    )
