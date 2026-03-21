"""Optional structured fields for scrape-focused answers."""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class ScrapeInsight(BaseModel):
    """Structured extraction the LLM may echo in JSON for downstream use."""

    source_url: str = Field(description="Primary URL analyzed")
    summary: str = Field(description="Short summary of what was on the page(s)")
    key_points: List[str] = Field(default_factory=list, description="Bullet facts extracted")
    tables_or_data_notes: Optional[str] = Field(
        default=None,
        description="If numeric/tabular data was found, describe it briefly",
    )
    follow_up_urls: List[str] = Field(
        default_factory=list,
        description="Other URLs worth fetching next",
    )
    confidence: str = Field(default="medium", description="low | medium | high")
    scraped_at: str = Field(default_factory=lambda: datetime.now().isoformat())
