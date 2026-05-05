from typing import List

from pydantic import BaseModel, Field


class FreelanceScopeReply(BaseModel):
    project_summary: str = Field(default="")
    deliverables: List[str] = Field(default_factory=list)
    milestones: List[str] = Field(
        default_factory=list,
        description="Ordered checkpoints with acceptance hints",
    )
    assumptions: List[str] = Field(default_factory=list)
    out_of_scope: List[str] = Field(default_factory=list)
    risks_open_questions: List[str] = Field(default_factory=list)
    payment_terms_notes: str = Field(
        default="",
        description="High-level reminder only—not legal advice",
    )
