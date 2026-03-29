"""
Multi-phase pipeline: Analyst → Red Team → Blue Team → Chair (structured JSON).
"""
from __future__ import annotations

import json
import re
from typing import Any, List, Optional, Tuple

from langchain_core.messages import HumanMessage, SystemMessage

from schemas import AdversarialReviewReport

SYS_ANALYST = """You are the Analyst. Decompose the user's proposal neutrally.
Output markdown with sections: Goals, Stakeholders, Key assumptions, Success metrics, Dependencies.
Do not judge yet; be precise and concise."""

SYS_RED = """You are the Red Team. Attack the proposal: find failure modes, abuse cases, second-order effects, and where incentives go wrong.
Rules: no illegal instructions; focus on legitimate stress testing. Output markdown bullets grouped by theme."""

SYS_BLUE = """You are the Blue Team. Respond to the Red Team: mitigations, guardrails, monitoring, phased rollout, and validation experiments.
Output markdown bullets; be concrete."""

SYS_CHAIR = """You are the Chair. Synthesize Analyst, Red Team, and Blue Team into one decision-ready view.
You MUST end your reply with a single JSON object ONLY (no markdown fences), matching exactly this shape:
{"analyst_summary":"string","red_team_risks":["string"],"blue_team_mitigations":["string"],"chair_verdict":"string","confidence":"low|medium|high","next_steps":["string"],"open_questions":["string"]}
Fill arrays with concise strings. analyst_summary should compress the Analyst's decomposition."""


def _content(msg: Any) -> str:
    return (getattr(msg, "content", None) or str(msg)).strip()


def _parse_report(text: str) -> Tuple[Optional[AdversarialReviewReport], str]:
    raw = text.strip()
    try:
        m = re.search(r"\{[\s\S]*\}\s*$", raw) or re.search(r"\{[\s\S]*\}", raw)
        if m:
            return AdversarialReviewReport(**json.loads(m.group())), raw
    except Exception:
        pass
    return None, raw


def run_adversarial_review(
    llm: Any,
    proposal: str,
    extra_context: str = "",
    verbose: bool = False,
) -> dict:
    """
    Run four LLM phases; return dict with phase transcripts and structured report (if parsed).
    """
    proposal = (proposal or "").strip()
    ctx = (extra_context or "").strip()
    user_base = f"## Proposal\n{proposal}\n"
    if ctx:
        user_base += f"\n## Additional context\n{ctx}\n"

    if verbose:
        print("Phase 1/4: Analyst...")

    a1 = llm.invoke(
        [SystemMessage(content=SYS_ANALYST), HumanMessage(content=user_base)]
    )
    analyst_text = _content(a1)

    if verbose:
        print("Phase 2/4: Red Team...")

    a2 = llm.invoke(
        [
            SystemMessage(content=SYS_RED),
            HumanMessage(
                content=user_base
                + "\n## Analyst output\n"
                + analyst_text
            ),
        ]
    )
    red_text = _content(a2)

    if verbose:
        print("Phase 3/4: Blue Team...")

    a3 = llm.invoke(
        [
            SystemMessage(content=SYS_BLUE),
            HumanMessage(
                content=user_base
                + "\n## Analyst output\n"
                + analyst_text
                + "\n## Red Team output\n"
                + red_text
            ),
        ]
    )
    blue_text = _content(a3)

    if verbose:
        print("Phase 4/4: Chair (structured synthesis)...")

    a4 = llm.invoke(
        [
            SystemMessage(content=SYS_CHAIR),
            HumanMessage(
                content=user_base
                + "\n## Analyst output\n"
                + analyst_text
                + "\n## Red Team output\n"
                + red_text
                + "\n## Blue Team output\n"
                + blue_text
            ),
        ]
    )
    chair_raw = _content(a4)
    structured, _ = _parse_report(chair_raw)

    return {
        "proposal": proposal,
        "analyst_markdown": analyst_text,
        "red_team_markdown": red_text,
        "blue_team_markdown": blue_text,
        "chair_raw": chair_raw,
        "structured": structured,
    }
