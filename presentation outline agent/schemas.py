from typing import List

from pydantic import BaseModel, Field


class DeckOutlineReply(BaseModel):
    title_options: List[str] = Field(default_factory=list)
    audience_and_goal: str = Field(default="")
    storyline_beats: List[str] = Field(
        default_factory=list,
        description="Narrative arc: setup → tension → resolution",
    )
    slides: List[str] = Field(
        default_factory=list,
        description="One line per slide: title — bullet intent",
    )
    speaker_notes_hints: List[str] = Field(default_factory=list)
    closing_cta: str = Field(default="")
