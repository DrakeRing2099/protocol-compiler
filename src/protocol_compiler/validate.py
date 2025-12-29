from __future__ import annotations

import re
from enum import Enum
from typing import List

from pydantic import BaseModel, Field

from .schemas import Domain, IntentFrame, ValidationStatus, ValidationResult

# -----------------------
# Heuristics (v1)
# -----------------------

_REJECT_PATTERNS = [
    r"\bmillionaire\b",
    r"\brich\b",
    r"\bwealthy\b",
    r"\bsuccessful\b",
    r"\bchange my life\b",
    r"\bfix my life\b",
    r"\bbe happy\b",
    r"\bget a girlfriend\b",
    r"\bcareer\b",
]

_VAGUE_SUCCESS_PATTERNS = [
    r"\bget better\b",
    r"\bimprove\b",
    r"\bunderstand well\b",
    r"\bmaster\b",
    r"\bbe good at\b",
    r"\blearn\b$",
]


def _matches_any(patterns: List[str], text: str) -> bool:
    t = text.strip().lower()
    return any(re.search(p, t) for p in patterns)


def validate_intent(intent: IntentFrame) -> ValidationResult:
    reasons: List[str] = []
    questions: List[str] = []

    # 1) Hard reject: unbounded / existential objectives
    if _matches_any(_REJECT_PATTERNS, intent.objective):
        return ValidationResult(
            status=ValidationStatus.REJECTED,
            reasons=[
                "Objective is not task-shaped (unbounded / life-goal).",
                "Reformulate as a bounded, time-scoped objective with measurable success.",
            ],
        )

    # 2) Sanity bounds
    if intent.time_horizon_days > 365:
        return ValidationResult(
            status=ValidationStatus.REJECTED,
            reasons=["Time horizon too large for v1 (must be <= 365 days)."],
        )

    # 3) Success definition must be testable-ish (v1 heuristic)
    if _matches_any(_VAGUE_SUCCESS_PATTERNS, intent.success_definition):
        questions.append(
            "Define success in a testable way (e.g., 'solve X problems', 'run Y km continuously', 'score Z on a mock')."
        )
        reasons.append("Success definition is too vague.")

    # 4) Domain-specific missing info
    if intent.domain == Domain.FITNESS:
        if not intent.starting_state:
            questions.append("What is your current level? (e.g., 'can run 2km', 'lift X kg', etc.)")
            reasons.append("Missing starting_state for fitness intent.")

        # Encourage explicit time constraints if none provided
        if not intent.constraints:
            questions.append("Any constraints? (minutes per day, days per week, injuries, equipment)")
            reasons.append("Missing constraints (optional but recommended).")

    if intent.domain in (Domain.STUDY, Domain.CODING):
        if not intent.constraints:
            questions.append("Any constraints? (available minutes/day, schedule limits, resources)")
            reasons.append("Missing constraints (optional but recommended).")

    # 5) Decide status
    if questions:
        return ValidationResult(
            status=ValidationStatus.NEEDS_CLARIFICATION,
            reasons=reasons,
            clarification_questions=questions,
        )

    return ValidationResult(status=ValidationStatus.VALID)
