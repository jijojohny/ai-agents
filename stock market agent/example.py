"""Example: stock data + analysis."""
import os

from dotenv import load_dotenv

from main import StockMarketAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

if __name__ == "__main__":
    agent = StockMarketAgent(provider="openai", model_name="gpt-4o-mini")
    agent.print_result(
        agent.chat(
            "Use tools: quote + profile + 2 news items for MSFT. Then 1-paragraph summary.",
            verbose=True,
        )
    )
