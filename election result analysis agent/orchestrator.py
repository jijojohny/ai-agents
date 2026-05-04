"""
Five-phase post-election analysis: intake → description → institutions → media literacy → JSON.

"AGI-style" here means multiple specialist passes with accumulated context—not literal AGI.
"""
from __future__ import annotations

import json
import re
from typing import Any, Optional, Tuple

from langchain_core.messages import HumanMessage, SystemMessage

from schemas import ElectionResultAnalysisReport

SYS_P1 = """You are the Results Intake specialist. The user will describe or paste **already-reported** election results.

Rules:
- List exactly what quantities/text you are treating as data (office, geography, vote totals, % reporting if given).
- If the user did not cite a source or date, flag it as UNKNOWN and ask what official feed it came from.
- Do **not** invent vote counts or winners not present in the user message.
Output markdown: Data inventory, Sources stated, Gaps."""

SYS_P2 = """You are the Descriptive Analyst. Using ONLY the intake + user message, summarize **purely descriptive** findings:
margins, turnout if provided, changes vs a prior baseline **only if** the user supplied comparable prior numbers.
No causal claims about demographics unless the user pasted demographic tables.
Output markdown with headings: Margins, Turnout, Shifts (or 'Not enough data')."""

SYS_P3 = """You are the Institutional Context specialist. Explain **generic** post-election processes
(certification, recount triggers, provisional ballots) at a high level. If the user named a jurisdiction, tailor cautiously
and say 'verify with official guidance—this is not legal advice.' Output markdown bullets."""

SYS_P4 = """You are the Media Literacy specialist. Given prior phases, explain how headlines or social posts might
over-interpret partial results, and what is still unknown until certification. Stay non-partisan. Markdown."""

SYS_P5 = """You consolidate into one JSON object for downstream tools. Reply with ONLY valid JSON (no markdown fences):
{"jurisdiction":"string","data_summary":"string","headline_findings":["string"],"margin_turnout_and_shift_notes":["string"],"institutional_process_notes":["string"],"media_narrative_caveats":["string"],"open_questions":["string"],"disclaimer":"Analysis of user-supplied or cited official data only. Not legal advice. Verify with certified election authorities."}
Arrays must be strings. No invented statistics."""


def _content(msg: Any) -> str:
    return (getattr(msg, "content", None) or str(msg)).strip()


def _parse(text: str) -> Tuple[Optional[ElectionResultAnalysisReport], str]:
    raw = text.strip()
    try:
        m = re.search(r"\{[\s\S]*\}\s*$", raw) or re.search(r"\{[\s\S]*\}", raw)
        if m:
            return ElectionResultAnalysisReport(**json.loads(m.group())), raw
    except Exception:
        pass
    return None, raw


def run_election_result_pipeline(
    llm: Any,
    results_and_context: str,
    extra_notes: str = "",
    verbose: bool = False,
) -> dict:
    body = (results_and_context or "").strip()
    notes = (extra_notes or "").strip()
    base = f"## Election results / context (user-provided)\n{body}\n"
    if notes:
        base += f"\n## Additional notes\n{notes}\n"

    def inv(sys_txt: str, suffix: str = "") -> str:
        return _content(
            llm.invoke([SystemMessage(content=sys_txt), HumanMessage(content=base + suffix)])
        )

    if verbose:
        print("Phase 1/5: Results intake...")
    p1 = inv(SYS_P1)

    if verbose:
        print("Phase 2/5: Descriptive analysis...")
    p2 = inv(SYS_P2, f"\n## Phase 1 (Intake)\n{p1}\n")

    if verbose:
        print("Phase 3/5: Institutional context...")
    p3 = inv(SYS_P3, f"\n## Phase 1\n{p1}\n\n## Phase 2\n{p2}\n")

    if verbose:
        print("Phase 4/5: Media literacy...")
    p4 = inv(SYS_P4, f"\n## Phase 1\n{p1}\n\n## Phase 2\n{p2}\n\n## Phase 3\n{p3}\n")

    if verbose:
        print("Phase 5/5: JSON synthesis...")
    p5 = inv(
        SYS_P5,
        f"\n## Phase 1\n{p1}\n\n## Phase 2\n{p2}\n\n## Phase 3\n{p3}\n\n## Phase 4\n{p4}\n",
    )

    structured, _ = _parse(p5)
    return {
        "input_excerpt": body[:500] + ("..." if len(body) > 500 else ""),
        "phase1_intake": p1,
        "phase2_descriptive": p2,
        "phase3_institutional": p3,
        "phase4_media_literacy": p4,
        "phase5_raw": p5,
        "structured": structured,
    }
