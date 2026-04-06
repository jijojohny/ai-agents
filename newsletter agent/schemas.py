"""Newsletter draft structure."""
from typing import List

from pydantic import BaseModel, Field


class NewsletterReply(BaseModel):
    subject_lines: List[str] = Field(default_factory=list, description="3 options")
    preview_text: str = Field(default="", description="Preheader")
    sections: List[str] = Field(
        default_factory=list,
        description="Section headings + 1–2 line intent each",
    )
    body_markdown: str = Field(default="", description="Full draft in markdown")
    cta: str = Field(default="", description="Primary call to action")
    unsubscribe_reminder: str = Field(
        default="Include compliant unsubscribe link in real sends.",
        description="Compliance note",
    )
