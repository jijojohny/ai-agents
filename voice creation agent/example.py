"""
Example usage for Voice Creation Agent.
"""
from main import VoiceCreationAgent


def example_generate_multiple_personas() -> None:
    agent = VoiceCreationAgent()

    text = (
        "Welcome to our product update. Today we are shipping faster performance, "
        "better reliability, and a smoother user experience."
    )

    personas = ["narrator", "teacher", "podcast_host"]
    results = agent.create_voice_for_people(text=text, persons=personas, filename_prefix="product_update")
    for result in results:
        agent.print_result(result)


def example_custom_persona() -> None:
    agent = VoiceCreationAgent()
    agent.add_persona(
        name="news_reader",
        voice="echo",
        style_hint="formal and informative news reading tone",
    )

    result = agent.create_voice(
        text="Breaking update: the team completed the new rollout successfully.",
        person="news_reader",
        filename="news_reader_demo.mp3",
    )
    agent.print_result(result)


if __name__ == "__main__":
    print("\nVOICE CREATION AGENT EXAMPLES\n")
    example_generate_multiple_personas()
    # example_custom_persona()
