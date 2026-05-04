import os
from dotenv import load_dotenv
from main import OpenSourceTriageAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = OpenSourceTriageAgent("openai", "gpt-4o-mini")
    a.print_result(a.chat("Bug: npm install fails on Node 18 with peer dep error (paste log).", verbose=True))
