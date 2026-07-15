from collections.abc import Callable
from typing import Protocol

from src.models import (
    Assertion,
    EvaluationResult,
    ModelResponse,
    PromptTest,
    TestResult,
)


class ModelClient(Protocol):
    """Interface required from any LLM provider client."""

    def generate(self, prompt: str) -> ModelResponse:
        ...


Evaluator = Callable[[str, Assertion], EvaluationResult]


class TestRunner:
    """Coordinates model execution and response evaluation."""

    def __init__(
            self,
            client: ModelClient,
            evaluator: Evaluator,
    ) -> None:
        self._client = client
        self._evaluator = evaluator

    def run_tests(
            self,
            test_cases: list[PromptTest],
    ) -> list[TestResult]:
        return [
            self.run_test(test_case)
            for test_case in test_cases
        ]

    def run_test(self, test_case: PromptTest) -> TestResult:
        model_response = self._client.generate(test_case.prompt)

        evaluation = self._evaluator(
            actual_response=model_response.content,
            assertion=test_case.assertion,
        )

        return TestResult(
            test_id=test_case.id,
            name=test_case.name,
            category=test_case.category,
            prompt=test_case.prompt,
            model=model_response.model,
            actual_response=model_response.content,
            status=evaluation.status,
            passed=evaluation.passed,
            assertion_type=evaluation.assertion_type,
            expected=evaluation.expected,
            reason=evaluation.reason,
            response_time_seconds=(
                model_response.response_time_seconds
            ),
            prompt_tokens=model_response.prompt_tokens,
            output_tokens=model_response.output_tokens,
        )
