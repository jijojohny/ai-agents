"""Structured output for viral post packages."""
from typing import List

from pydantic import BaseModel, Field


class ViralPostReply(BaseModel):
    primary_post: str = Field(description="Main single-post draft")
    alternate_versions: List[str] = Field(
        default_factory=list,
        description="Additional variants or hooks",
    )
    thread_outline: List[str] = Field(
        default_factory=list,
        description="Optional thread: one bullet per post",
    )
    hashtags: List[str] = Field(
        default_factory=list,
        description="Optional hashtags (many niches use 0–2)",
    )
    posting_tips: List[str] = Field(
        default_factory=list,
        description="Timing, reply strategy, or polish tips",
    )
