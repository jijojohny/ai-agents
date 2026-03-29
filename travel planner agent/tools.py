"""Planning helpers (no live booking APIs)."""
from __future__ import annotations

from langchain_core.tools import tool


@tool
def trip_constraint_checklist() -> str:
    """Remind the user of common inputs for a useful itinerary."""
    return (
        "Useful inputs:\n"
        "- Dates, pace (relaxed vs packed), budget band\n"
        "- Home base(s) / mobility (walk, transit, car)\n"
        "- Interests (food, museums, nature)\n"
        "- Diet, mobility, or accessibility needs\n"
        "- Visa/entry basics (user must verify official sources)"
    )


@tool
def jet_lag_quick_tips(hours_offset: str = "6") -> str:
    """Generic jet lag tips; hours_offset is informational only."""
    _ = hours_offset
    return (
        "Generic tips: shift sleep 30–60 min/day before trip if possible; "
        "seek daylight after arrival; hydrate; avoid all-nighters before long haul. "
        "Not medical advice."
    )


def get_travel_planner_tools():
    return [trip_constraint_checklist, jet_lag_quick_tips]
