import os
from dotenv import load_dotenv
from main import EventPlanningAgent

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))
if __name__ == "__main__":
    a = EventPlanningAgent("openai", "gpt-4o-mini")
    a.print_result(
        a.chat(
            "Community meetup: 2-hour evening, 120 attendees, venue has bar and PA.",
            verbose=True,
        )
    )
