"""
Multi-phase incident response: Triage → Technical → Comms → Consolidated JSON.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional, Tuple

from langchain_core.messages import HumanMessage, SystemMessage

from schemas import IncidentResponseReport

SYS_TRIAGE = """You are an incident commander assistant focused on TRIAGE.
From the report: summarize symptoms, blast radius, customer impact, and likely severity (sev1–sev4 or unknown).
Output markdown: Summary, Impact, Severity hypothesis, Unknowns to confirm."""

SYS_TECH = """You are a senior engineer during an incident. Given triage, propose technical steps:
containment, evidence to collect, rollback/feature-flag options, communication with infra/vendor, validation of fix.
Output markdown bullet lists: Immediate, Investigation, Mitigation, Recovery, Verification."""

SYS_COMMS = """You are comms lead. Draft:
1) Internal update (Slack style, factual, no blame)
2) External/customer update OR say "defer" if too early
Use markdown with headings Internal and External."""

SYS_CHAIR = """You consolidate triage, technical, and comms drafts into one machine-readable report.
End with a single JSON object ONLY (no markdown fences), shape:
{"incident_title":"string","triage_summary":"string","severity":"sev1|sev2|sev3|sev4|unknown","immediate_actions":["string"],"technical_steps":["string"],"internal_comms_draft":"string","external_comms_draft":"string","timeline_suggested":["string"],"post_incident_followups":["string"]}
Merge and dedupe steps; keep language professional."""


def _content(msg: Any) -> str:
    return (getattr(msg, "content", None) or str(msg)).strip()


def _parse_report(text: str) -> Tuple[Optional[IncidentResponseReport], str]:
    raw = text.strip()
    try:
        m = re.search(r"\{[\s\S]*\}\s*$", raw) or re.search(r"\{[\s\S]*\}", raw)
        if m:
            return IncidentResponseReport(**json.loads(m.group())), raw
    except Exception:
        pass
    return None, raw


def run_incident_pipeline(
    llm: Any,
    incident_description: str,
    extra_context: str = "",
    verbose: bool = False,
) -> dict:
    desc = (incident_description or "").strip()
    ctx = (extra_context or "").strip()
    base = f"## Incident report\n{desc}\n"
    if ctx:
        base += f"\n## Context\n{ctx}\n"

    if verbose:
        print("Phase 1/4: Triage...")

    t1 = llm.invoke([SystemMessage(content=SYS_TRIAGE), HumanMessage(content=base)])
    triage_text = _content(t1)

    if verbose:
        print("Phase 2/4: Technical...")

    t2 = llm.invoke(
        [
            SystemMessage(content=SYS_TECH),
            HumanMessage(
                content=base
                + "\n## Triage output\n"
                + triage_text
            ),
        ]
    )
    tech_text = _content(t2)

    if verbose:
        print("Phase 3/4: Comms...")

    t3 = llm.invoke(
        [
            SystemMessage(content=SYS_COMMS),
            HumanMessage(
                content=base
                + "\n## Triage output\n"
                + triage_text
                + "\n## Technical output\n"
                + tech_text
            ),
        ]
    )
    comms_text = _content(t3)

    if verbose:
        print("Phase 4/4: Consolidation (JSON)...")

    t4 = llm.invoke(
        [
            SystemMessage(content=SYS_CHAIR),
            HumanMessage(
                content=base
                + "\n## Triage output\n"
                + triage_text
                + "\n## Technical output\n"
                + tech_text
                + "\n## Comms output\n"
                + comms_text
            ),
        ]
    )
    chair_raw = _content(t4)
    structured, _ = _parse_report(chair_raw)

    return {
        "incident_description": desc,
        "triage_markdown": triage_text,
        "technical_markdown": tech_text,
        "comms_markdown": comms_text,
        "synthesis_raw": chair_raw,
        "structured": structured,
    }
