from protocol_compiler.schemas import Domain, IntentFrame
from protocol_compiler.validate import ValidationStatus, validate_intent


def test_rejects_unbounded_goal():
    intent = IntentFrame(
        objective="I want to become a millionaire",
        domain=Domain.GENERAL,
        time_horizon_days=30,
        success_definition="Become rich",
    )
    res = validate_intent(intent)
    assert res.status == ValidationStatus.REJECTED


def test_needs_clarification_for_vague_success():
    intent = IntentFrame(
        objective="Prepare for Codeforces Div 2",
        domain=Domain.CODING,
        time_horizon_days=14,
        success_definition="Get better",
    )
    res = validate_intent(intent)
    assert res.status == ValidationStatus.NEEDS_CLARIFICATION
    assert len(res.clarification_questions) >= 1


def test_valid_intent_passes():
    intent = IntentFrame(
        objective="Prepare for Codeforces Div 2",
        domain=Domain.CODING,
        time_horizon_days=14,
        constraints=["90 min/day"],
        success_definition="Solve 4/6 problems in a Div 2 contest",
    )
    res = validate_intent(intent)
    assert res.status == ValidationStatus.VALID
