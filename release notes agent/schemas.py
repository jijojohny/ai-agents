"""Release notes structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class ReleaseNotesReply(BaseModel):
    version: Optional[str] = Field(default=None, description="Semver or label if provided")
    headline: str = Field(description="One-line release headline")
    highlights: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    fixes: List[str] = Field(default_factory=list)
    breaking_changes: List[str] = Field(default_factory=list)
    upgrade_notes: List[str] = Field(default_factory=list)
    known_issues: List[str] = Field(default_factory=list)
    markdown_body: str = Field(default="", description="Customer-facing markdown release notes")
