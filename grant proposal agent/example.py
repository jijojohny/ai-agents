import os
from dotenv import load_dotenv
from main import GrantProposalAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = GrantProposalAgent("openai", "gpt-4o-mini")
    a.print_result(a.chat("RFP asks for logic model; we run youth coding workshops in 3 cities.", verbose=True))
