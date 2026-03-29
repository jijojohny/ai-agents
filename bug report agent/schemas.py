"""Structured bug report output."""
from typing import List

from pydantic import BaseModel, Field


class BugReportReply(BaseModel):
    title: str = Field(description="Short issue title for trackers")
    summary: str = Field(description="One-paragraph overview")
    steps_to_reproduce: List[str] = Field(default_factory=list, description="Numbered-style steps")
    expected_behavior: str = Field(default="", description="What should happen")
    actual_behavior: str = Field(default="", description="What happens instead")
    environment_notes: List[str] = Field(
        default_factory=list,
        description="Versions, OS, URL, feature flags, etc.",
    )
    severity_hint: str = Field(default="", description="Rough priority from tools or reasoning")
    suggested_labels: List[str] = Field(
        default_factory=list,
        description="e.g. mobile, checkout, api",
    )
