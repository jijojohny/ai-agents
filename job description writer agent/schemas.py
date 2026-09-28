"""Job description structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class JobDescriptionReply(BaseModel):
    title_options: List[str] = Field(default_factory=list, description="Suggested job titles")
    summary: str = Field(description="Role overview paragraph")
    responsibilities: List[str] = Field(default_factory=list)
    requirements_must: List[str] = Field(default_factory=list, description="Must-have qualifications")
    requirements_nice: List[str] = Field(default_factory=list, description="Nice-to-have qualifications")
    compensation_notes: Optional[str] = Field(
        default=None,
        description="How to talk about pay/benefits without inventing numbers",
    )
    inclusivity_notes: List[str] = Field(
        default_factory=list,
        description="Wording to avoid bias / improve accessibility of the listing",
    )
    open_questions: List[str] = Field(
        default_factory=list,
        description="What hiring managers should confirm before posting",
    )
