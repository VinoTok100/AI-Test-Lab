from unittest.mock import Mock

from src.models import (
    Assertion,
    AssertionType,
    EvaluationResult,
    EvaluationStatus,
    ModelResponse,
    PromptTest,
)
from src.test_runner import TestRunner as Runner


def test_runner_executes_prompt_and_returns_test_result():
    test_case = PromptTest(
        id="FUNC-001",
        name="Python creator",
        category="functional",
        prompt="Who created Python?",
        assertion=Assertion(
            type=AssertionType.CONTAINS,
            expected="Guido van Rossum",
        ),
    )

    mock_client = Mock()
    mock_client.generate.return_value = ModelResponse(
        model="llama3.1:latest",
        content="Python was created by Guido van Rossum.",
        response_time_seconds=0.5,
        prompt_tokens=10,
        output_tokens=9,
    )

    mock_evaluator = Mock()
    mock_evaluator.return_value = EvaluationResult(
        passed=True,
        status=EvaluationStatus.PASS,
        assertion_type=AssertionType.CONTAINS,
        expected="Guido van Rossum",
        reason="Expected text was found.",
    )

    runner = Runner(
        client=mock_client,
        evaluator=mock_evaluator,
    )

    result = runner.run_test(test_case)

    assert result.test_id == "FUNC-001"
    assert result.status == EvaluationStatus.PASS
    assert result.passed is True
    assert result.model == "llama3.1:latest"

    mock_client.generate.assert_called_once_with(
        "Who created Python?"
    )

