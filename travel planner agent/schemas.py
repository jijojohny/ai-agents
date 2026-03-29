"""Structured trip plan."""
from typing import List

from pydantic import BaseModel, Field


class DayPlan(BaseModel):
    day_label: str = Field(description="e.g. Day 1 — Arrival")
    bullets: List[str] = Field(default_factory=list, description="Activities or blocks")


class TravelPlanReply(BaseModel):
    trip_summary: str = Field(description="One paragraph overview")
    days: List[DayPlan] = Field(default_factory=list, description="Day-by-day outline")
    budget_notes: List[str] = Field(default_factory=list)
    transport_tips: List[str] = Field(default_factory=list)
    safety_and_etiquette: List[str] = Field(default_factory=list)
