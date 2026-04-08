"""Structured resume tailoring output."""
from typing import List

from pydantic import BaseModel, Field


class ResumeTailorReply(BaseModel):
    role_alignment_summary: str = Field(description="How your background maps to the JD")
    keywords_from_jd: List[str] = Field(
        default_factory=list,
        description="Terms to reflect honestly in wording",
    )
    revised_bullets: List[str] = Field(
        default_factory=list,
        description="Tailored achievement bullets (no fabricated facts)",
    )
    professional_summary_suggestion: str = Field(
        default="",
        description="2–4 sentence summary option",
    )
    gaps_or_questions: List[str] = Field(
        default_factory=list,
        description="Missing proof or info to gather from the user",
    )
    integrity_note: str = Field(
        default="Only claim what you can defend in an interview.",
    )
