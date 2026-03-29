"""Consolidated incident response package from the synthesis phase."""
from typing import List

from pydantic import BaseModel, Field


class IncidentResponseReport(BaseModel):
    incident_title: str = Field(description="Short title for the incident")
    triage_summary: str = Field(description="What is happening and user/customer impact")
    severity: str = Field(
        default="unknown",
        description="sev1 | sev2 | sev3 | sev4 | unknown (model may use variants)",
    )
    immediate_actions: List[str] = Field(
        default_factory=list,
        description="First 0–60 minute stabilization steps",
    )
    technical_steps: List[str] = Field(
        default_factory=list,
        description="Investigation, containment, recovery",
    )
    internal_comms_draft: str = Field(
        default="",
        description="Slack/email style update for internal stakeholders",
    )
    external_comms_draft: str = Field(
        default="",
        description="Status page or customer email draft; empty if not appropriate yet",
    )
    timeline_suggested: List[str] = Field(
        default_factory=list,
        description="Suggested timeline bullets for the incident log",
    )
    post_incident_followups: List[str] = Field(
        default_factory=list,
        description="Postmortem, action items, preventive work",
    )
