import os
from dotenv import load_dotenv
from main import PodcastShowNotesAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = PodcastShowNotesAgent("openai", "gpt-4o-mini")
    a.print_result(a.chat("Topic: climate tech funding winter. Solo 20 min.", verbose=True))
