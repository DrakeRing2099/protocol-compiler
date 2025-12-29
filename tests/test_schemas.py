# tests/test_schemas.py

import pytest
from pydantic import ValidationError

from protocol_compiler.schemas import (
    Domain,
    IntentFrame,
    ProtocolDay,
    ProtocolPlan,
    Task,
    TaskType,
)


def test_intentframe_valid_minimal():
    intent = IntentFrame(
        objective="Prepare for Codeforces Div 2",
        domain=Domain.CODING,
        time_horizon_days=14,
        success_definition="Can solve 4/6 problems in a Div 2",
    )
    assert intent.objective.startswith("Prepare")
    assert intent.time_horizon_days == 14
    assert intent.constraints == []
    assert intent.starting_state is None


def test_intentframe_rejects_nonpositive_time_horizon():
    with pytest.raises(ValidationError):
        IntentFrame(
            objective="Learn eigenvalues",
            domain=Domain.STUDY,
            time_horizon_days=0,  # invalid
            success_definition="Solve tutorial sheet questions",
        )

    with pytest.raises(ValidationError):
        IntentFrame(
            objective="Learn eigenvalues",
            domain=Domain.STUDY,
            time_horizon_days=-7,  # invalid
            success_definition="Solve tutorial sheet questions",
        )


def test_task_valid_with_duration_only():
    t = Task(type=TaskType.CONCEPTUAL, duration_min=60)
    assert t.duration_min == 60
    assert t.count is None


def test_task_valid_with_count_only():
    t = Task(type=TaskType.PRACTICE, count=10)
    assert t.count == 10
    assert t.duration_min is None


def test_task_rejects_nonpositive_duration():
    with pytest.raises(ValidationError):
        Task(type=TaskType.REVIEW, duration_min=0)

    with pytest.raises(ValidationError):
        Task(type=TaskType.REVIEW, duration_min=-30)


def test_task_rejects_nonpositive_count():
    with pytest.raises(ValidationError):
        Task(type=TaskType.PRACTICE, count=0)

    with pytest.raises(ValidationError):
        Task(type=TaskType.PRACTICE, count=-3)


def test_protocol_day_requires_at_least_one_task():
    with pytest.raises(ValidationError):
        ProtocolDay(day=1, tasks=[])


def test_protocol_plan_roundtrip_json():
    intent = IntentFrame(
        objective="Build running stamina to 10km",
        domain=Domain.FITNESS,
        time_horizon_days=28,
        starting_state="Can run 2km comfortably",
        constraints=["evenings only", "max 30 min/day"],
        success_definition="Complete 10km continuous run",
    )

    day1 = ProtocolDay(
        day=1,
        focus="Baseline + easy run",
        tasks=[
            Task(type=TaskType.EXECUTE, duration_min=20, description="Easy run"),
            Task(type=TaskType.REVIEW, duration_min=10, description="Log how it felt"),
        ],
    )

    plan = ProtocolPlan(intent=intent, days=[day1])

    payload = plan.model_dump_json(indent=2)
    plan2 = ProtocolPlan.model_validate_json(payload)

    assert plan2.intent.objective == intent.objective
    assert plan2.days[0].day == 1
    assert plan2.days[0].tasks[0].type == TaskType.EXECUTE
