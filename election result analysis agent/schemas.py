"""Structured output from the synthesis phase (post-election analysis)."""
from typing import List

from pydantic import BaseModel, Field


class ElectionResultAnalysisReport(BaseModel):
    jurisdiction: str = Field(
        default="",
        description="Office/region the user specified, e.g. US state, national, local race",
    )
    data_summary: str = Field(
        description="What numbers/text were analyzed and their stated source/date",
    )
    headline_findings: List[str] = Field(
        default_factory=list,
        description="Factual takeaways grounded only in supplied data",
    )
    margin_turnout_and_shift_notes: List[str] = Field(
        default_factory=list,
        description="Margins, turnout, swings—only if user provided comparable figures",
    )
    institutional_process_notes: List[str] = Field(
        default_factory=list,
        description="Certification, recounts, provisional ballots—generic education unless user cites law",
    )
    media_narrative_caveats: List[str] = Field(
        default_factory=list,
        description="How framing can outrun evidence; what remains unknown",
    )
    open_questions: List[str] = Field(default_factory=list)
    disclaimer: str = Field(
        default="Analysis of user-supplied or cited official data only. Not legal advice. Verify with certified election authorities.",
    )
