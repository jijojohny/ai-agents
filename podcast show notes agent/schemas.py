from typing import List

from pydantic import BaseModel, Field


class PodcastNotesReply(BaseModel):
    episode_title_options: List[str] = Field(default_factory=list)
    one_line_hook: str = Field(default="")
    summary: str = Field(default="", description="Listener-facing summary")
    chapters: List[str] = Field(
        default_factory=list,
        description="Timestamp placeholders e.g. [00:00] Intro — user fills real times",
    )
    key_takeaways: List[str] = Field(default_factory=list)
    links_and_resources: List[str] = Field(default_factory=list)
    show_notes_body_markdown: str = Field(default="", description="Publish-ready draft")
