from src.models import (
    Assertion,
    AssertionType,
    EvaluationResult,
    EvaluationStatus,
)


def evaluate_response(
        actual_response: str,
        assertion: Assertion,
) -> EvaluationResult:
    actual = actual_response.strip().lower()
    expected = assertion.expected.strip().lower()

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
        status=EvaluationStatus.PASS if passed else EvaluationStatus.FAIL,
        assertion_type=assertion.type,
        expected=assertion.expected,
        reason="Evaluation completed.",
    )

from pydantic import BaseModel, Field


class OllamaMetrics(BaseModel):
    """Performance measurements returned by Ollama."""

    prompt_tokens: int = 0
    response_tokens: int = 0

    prompt_latency_seconds: float = 0.0
    generation_latency_seconds: float = 0.0
    total_latency_seconds: float = 0.0
    model_load_seconds: float = 0.0

    prompt_tokens_per_second: float = 0.0
    generation_tokens_per_second: float = 0.0

    peak_ram_mb: float | None = None
    peak_vram_mb: float | None = None


class OllamaResponse(BaseModel):
    """Generated response and its performance metrics."""

    text: str
    model: str
    metrics: OllamaMetrics
