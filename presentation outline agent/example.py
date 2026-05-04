import os
from dotenv import load_dotenv
from main import PresentationOutlineAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = PresentationOutlineAgent("openai", "gpt-4o-mini")
    a.print_result(a.chat("Lunch & learn: intro to LangGraph, 30 min, mixed skill levels.", verbose=True))
