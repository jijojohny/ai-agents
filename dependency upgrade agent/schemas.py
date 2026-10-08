"""Dependency upgrade planning structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class DependencyUpgradeReply(BaseModel):
    ecosystem: str = Field(default="", description="npm, pip, cargo, go, maven, etc.")
    packages: List[str] = Field(default_factory=list, description="Packages / version jumps discussed")
    upgrade_order: List[str] = Field(default_factory=list)
    breaking_change_watchlist: List[str] = Field(default_factory=list)
    test_plan: List[str] = Field(default_factory=list)
    rollback_notes: List[str] = Field(default_factory=list)
    security_notes: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    summary: Optional[str] = Field(default=None)
