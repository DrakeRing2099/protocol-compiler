from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Tuple

from .schemas import Domain


TIME_RE = re.compile(r"(\d+)\s*(day|days|week|weeks)\b", re.I)

# matches "90 min/day", "2 hours/day", "2h/day"
BUDGET_RE = re.compile(
    r"(\d+)\s*(min|mins|minute|minutes|h|hr|hrs|hour|hours)\s*/\s*day\b",
    re.I,
)

DOMAIN_KEYWORDS = {
    Domain.CODING: ["codeforces", "leetcode", "dsa", "contest", "div2", "div 2", "cp"],
    Domain.STUDY: ["study", "learn", "chapter", "topic", "eigen", "exam", "sheet"],
    Domain.FITNESS: ["run", "marathon", "gym", "workout", "lift", "stamina"],
}


def _mask_span(text: str, start: int, end: int) -> str:
    # Replace span with spaces so indices of other matches stay valid enough
    return text[:start] + (" " * (end - start)) + text[end:]


def _normalize_budget(value: int, unit: str) -> str:
    u = unit.lower()
    if u in ("h", "hr", "hrs", "hour", "hours"):
        return f"{value * 60} min/day"
    return f"{value} min/day"


def _extract_time_horizon_days(text: str) -> Tuple[Optional[int], str, List[Dict[str, Any]]]:
    tokens = []
    m = TIME_RE.search(text)
    if not m:
        return None, text, tokens

    n = int(m.group(1))
    unit = m.group(2).lower()
    days = n * 7 if "week" in unit else n

    tokens.append({"type": "time_horizon", "value": days, "span": (m.start(), m.end()), "raw": m.group(0)})
    text = _mask_span(text, m.start(), m.end())
    return days, text, tokens


def _extract_budget_constraint(text: str) -> Tuple[Optional[str], str, List[Dict[str, Any]]]:
    tokens = []
    m = BUDGET_RE.search(text)
    if not m:
        return None, text, tokens

    value = int(m.group(1))
    unit = m.group(2)
    normalized = _normalize_budget(value, unit)

    tokens.append({"type": "budget", "value": normalized, "span": (m.start(), m.end()), "raw": m.group(0)})
    text = _mask_span(text, m.start(), m.end())
    return normalized, text, tokens


def _guess_domain(text: str) -> Optional[Domain]:
    t = text.lower()
    best: Optional[Domain] = None
    best_hits = 0

    for dom, kws in DOMAIN_KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in t)
        if hits > best_hits:
            best_hits = hits
            best = dom

    return best if best_hits > 0 else None


def lex_intent(text: str) -> Dict[str, Any]:
    """
    v1 heuristic lexer:
    - extracts a small set of tokens (time horizon, budget)
    - domain is keyword-guessed
    - objective_raw is the remainder after token removal (NOT 'intelligently extracted')
    """
    original = text
    tokens: List[Dict[str, Any]] = []
    constraints: List[str] = []

    time_days, text, toks = _extract_time_horizon_days(text)
    tokens.extend(toks)

    budget, text, toks = _extract_budget_constraint(text)
    tokens.extend(toks)
    if budget:
        constraints.append(budget)

    domain = _guess_domain(original)

    # objective is "everything that wasn't a token"
    objective_raw = " ".join(text.replace(",", " ").split()).strip()
    if not objective_raw:
        objective_raw = original.strip()

    return {
        "objective_raw": objective_raw,
        "time_horizon_days": time_days,
        "constraints": constraints,
        "domain_guess": domain,
        "tokens": tokens,
    }
