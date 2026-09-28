"""SEO content brief structured reply."""
from typing import List, Optional

from pydantic import BaseModel, Field


class SEOContentBriefReply(BaseModel):
    primary_keyword: str = Field(description="Main target query/keyword")
    secondary_keywords: List[str] = Field(default_factory=list)
    search_intent: str = Field(description="informational | transactional | navigational | commercial")
    title_options: List[str] = Field(default_factory=list)
    meta_description: Optional[str] = Field(default=None, description="~150–160 char suggestion")
    outline_h2: List[str] = Field(default_factory=list, description="Proposed H2 sections")
    people_also_ask: List[str] = Field(default_factory=list)
    internal_link_ideas: List[str] = Field(default_factory=list)
    risks_notes: List[str] = Field(
        default_factory=list,
        description="Keyword stuffing, YMYL caution, missing data, etc.",
    )
