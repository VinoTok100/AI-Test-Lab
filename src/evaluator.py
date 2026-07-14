from src.models import (
    Assertion,
    AssertionType,
    EvaluationStatus,
    EvaluationResult,
)


def evaluate_response(
    actual_response: str,
    assertion: Assertion,
) -> EvaluationResult:
    actual = actual_response.lower().strip()
    expected = assertion.expected.lower().strip()

    if assertion.type == AssertionType.CONTAINS:
        passed = expected in actual

    elif assertion.type == AssertionType.NOT_CONTAINS:
        passed = expected not in actual

    elif assertion.type == AssertionType.EQUALS:
        passed = actual == expected

    else:
        raise ValueError(f"Unsupported assertion type: {assertion.type}")

    return EvaluationResult(
        passed=passed,
        #status=EvaluationResult.PASS if passed else EvaluationResult.FAIL,
        status=EvaluationStatus.PASS if passed else EvaluationStatus.FAIL,
        assertion_type=assertion.type,
        expected=assertion.expected,
        reason="Evaluation completed.",
    )