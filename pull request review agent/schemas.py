"""Structured PR review output."""
from typing import List

from pydantic import BaseModel, Field


class ReviewComment(BaseModel):
    file_or_area: str = Field(default="", description="File, module, or theme")
    severity: str = Field(default="suggestion", description="blocking|important|suggestion|praise")
    comment: str = Field(description="Actionable review text")


class PRReviewReply(BaseModel):
    summary: str = Field(description="High-level read on the change")
    strengths: List[str] = Field(default_factory=list)
    comments: List[ReviewComment] = Field(default_factory=list)
    test_and_qa_gaps: List[str] = Field(default_factory=list)
    security_and_privacy_notes: List[str] = Field(default_factory=list)
    merge_recommendation: str = Field(
        default="needs_follow_up",
        description="approve|request_changes|needs_follow_up|comment_only",
    )
