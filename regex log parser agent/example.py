import os
from dotenv import load_dotenv
from main import RegexLogParserAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = RegexLogParserAgent("openai", "gpt-4o-mini")
    a.print_result(
        a.chat(
            'Sample: 2025-01-02T12:00:00Z level=ERROR req=abc-123 msg="timeout"',
            verbose=True,
        )
    )
