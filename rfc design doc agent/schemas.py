"""RFC / design doc structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class RfcDesignDocReply(BaseModel):
    title: str = Field(default="")
    status: str = Field(default="draft", description="draft | proposed | accepted | rejected")
    problem: str = Field(default="")
    goals: List[str] = Field(default_factory=list)
    non_goals: List[str] = Field(default_factory=list)
    proposal: str = Field(default="")
    alternatives: List[str] = Field(default_factory=list)
    risks: List[str] = Field(default_factory=list)
    open_questions: List[str] = Field(default_factory=list)
    markdown_rfc: Optional[str] = Field(default=None)
