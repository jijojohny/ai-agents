from typing import List

from pydantic import BaseModel, Field


class OSSTriageReply(BaseModel):
    issue_summary: str = Field(default="")
    suggested_labels: List[str] = Field(default_factory=list)
    first_reply_markdown: str = Field(default="", description="Welcoming, asks for repro if needed")
    maintainer_checklist: List[str] = Field(
        default_factory=list,
        description="Duplicates, docs, repro, severity",
    )
    security_note: str = Field(
        default="If vulnerability: use private disclosure per SECURITY.md; do not post exploits publicly.",
    )
