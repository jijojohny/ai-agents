"""Optional structured equity analysis summary."""
from typing import List, Optional

from pydantic import BaseModel, Field


class StockAnalysisReply(BaseModel):
    symbol: str = Field(description="Primary ticker discussed")
    headline: str = Field(description="One-line takeaway")
    summary: str = Field(description="Narrative grounded in fetched data")
    key_metrics: List[str] = Field(
        default_factory=list,
        description="Bullets citing numbers from tools",
    )
    risk_factors: List[str] = Field(
        default_factory=list,
        description="Volatility, data gaps, macro, concentration, etc.",
    )
    disclaimer: str = Field(
        default="Not investment advice. Data may be delayed or incomplete.",
        description="Compliance-style reminder",
    )
    data_sources_note: Optional[str] = Field(
        default=None,
        description="Which tools or feeds were used",
    )
