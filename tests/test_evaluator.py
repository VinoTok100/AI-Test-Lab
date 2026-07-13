

from src.evaluator import evaluate_response
from src.models import Assertion, TestStatus


def test_contains_passes():
    assertion = Assertion(
        type="contains",
        expected="Guido van Rossum",
    )

    result = evaluate_response(
        actual_response="Python was created by Guido van Rossum.",
        assertion=assertion,
    )

    assert result.passed is True
    assert result.status == TestStatus.PASS


def test_contains_fails():
    assertion = Assertion(
        type="contains",
        expected="Guido van Rossum",
    )

    result = evaluate_response(
        actual_response="Python is a programming language.",
        assertion=assertion,
    )

    assert result.passed is False
    assert result.status == TestStatus.FAIL