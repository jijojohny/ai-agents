from typing import List

from pydantic import BaseModel, Field


class GrantOutlineReply(BaseModel):
    funder_fit_summary: str = Field(default="", description="Alignment to stated RFP goals")
    problem_statement: str = Field(default="")
    objectives: List[str] = Field(default_factory=list)
    methods_workplan: List[str] = Field(default_factory=list)
    outcomes_and_metrics: List[str] = Field(default_factory=list)
    timeline_milestones: List[str] = Field(default_factory=list)
    budget_outline: List[str] = Field(
        default_factory=list,
        description="Categories only unless user gave numbers",
    )
    evaluation_risks: List[str] = Field(default_factory=list)
    disclaimer: str = Field(
        default="Drafting aid only—not legal, financial, or compliance approval. Match funder templates exactly.",
    )
