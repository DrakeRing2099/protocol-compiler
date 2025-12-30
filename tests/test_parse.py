import pytest

from protocol_compiler.parse import lex_intent
from protocol_compiler.schemas import Domain


def test_extracts_days():
    out = lex_intent("Prepare for Codeforces Div 2 in 14 days")
    assert out["time_horizon_days"] == 14


def test_extracts_weeks_as_days():
    out = lex_intent("Run training plan for 4 weeks")
    assert out["time_horizon_days"] == 28


def test_extracts_budget_minutes_per_day():
    out = lex_intent("Prepare for Div2 in 14 days, 90 min/day")
    assert out["time_horizon_days"] == 14
    assert "90 min/day" in out["constraints"]


def test_budget_and_time_do_not_conflict():
    # Ensure budget regex doesn't accidentally eat the "4" from "4 weeks"
    out = lex_intent("Prepare for Div2 for 4 weeks, 30 min/day")
    assert out["time_horizon_days"] == 28
    assert "30 min/day" in out["constraints"]


def test_domain_guess_coding():
    out = lex_intent("Prepare for Codeforces Div 2 in 14 days")
    assert out["domain_guess"] == Domain.CODING


def test_domain_guess_study():
    out = lex_intent("Study eigenvalues this week")
    assert out["domain_guess"] == Domain.STUDY


def test_objective_is_remainder_after_token_removal():
    out = lex_intent("I want to prepare for Codeforces Div 2 in 14 days, 90 min/day")
    obj = out["objective_raw"].lower()
    assert "14" not in obj
    assert "90" not in obj
    assert "codeforces" in obj
