"""
Tools for meeting note extraction and risk hinting.
"""
from __future__ import annotations


from langchain_core.tools import tool


@tool
def extract_action_items(notes: str) -> str:
    """Extract rough action items from raw notes using simple line heuristics."""
    lines = [ln.strip("-* \t") for ln in (notes or "").splitlines() if ln.strip()]
    candidates = []
    markers = ("action", "todo", "follow up", "owner", "due", "will", "needs to")
    for line in lines:
        low = line.lower()
        if any(m in low for m in markers):
            candidates.append(line)
    if not candidates:
        return "No explicit action-item lines found."
    return "Potential action items:\n" + "\n".join(f"- {c}" for c in candidates[:12])


@tool
def detect_risks(notes: str) -> str:
    """Flag common delivery/project risk signals from meeting notes."""
    text = (notes or "").lower()
    risks = []
    if any(k in text for k in ("delay", "blocked", "slip", "postpone")):
        risks.append("Schedule risk detected")
    if any(k in text for k in ("bug", "defect", "incident", "outage")):
        risks.append("Quality/reliability risk detected")
    if any(k in text for k in ("unknown", "unclear", "tbd", "not decided")):
        risks.append("Scope/decision ambiguity detected")
    if any(k in text for k in ("dependency", "vendor", "external")):
        risks.append("External dependency risk detected")
    return "\n".join(risks) if risks else "No obvious risk keywords detected."


def get_meeting_notes_tools():
    return [extract_action_items, detect_risks]
