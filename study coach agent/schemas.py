"""Study materials from notes or topics."""
from typing import List

from pydantic import BaseModel, Field


class Flashcard(BaseModel):
    front: str = Field(description="Question or prompt")
    back: str = Field(description="Answer or explanation")


class StudyPackReply(BaseModel):
    topic_summary: str = Field(description="Short synthesis of what to learn")
    flashcards: List[Flashcard] = Field(default_factory=list)
    practice_questions: List[str] = Field(
        default_factory=list,
        description="Open-ended or short-answer prompts",
    )
    study_schedule_hint: List[str] = Field(
        default_factory=list,
        description="Suggested sessions or spaced repetition hints",
    )
