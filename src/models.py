from datetime import datetime, timezone
from enum import StrEnum

from pydantic import BaseModel, Field


class AssertionType(StrEnum):
    """Supported methods for evaluating an AI response."""

    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    EQUALS = "equals"


class EvaluationStatus(StrEnum):
    """Possible outcomes of an AI test."""

    PASS = "PASS"
    FAIL = "FAIL"
    ERROR = "ERROR"


class Assertion(BaseModel):
    """Defines how the model response should be evaluated."""

    type: AssertionType
    expected: str = Field(min_length=1)


class PromptTest(BaseModel):
    """Represents one AI test case loaded from the prompt file."""

    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    prompt: str = Field(min_length=1)
    assertion: Assertion


class ModelResponse(BaseModel):
    """Represents the raw response and metrics returned by an LLM."""

    model: str
    content: str
    response_time_seconds: float = Field(ge=0)
    prompt_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)


class EvaluationResult(BaseModel):
    """Represents the result of evaluating an AI response."""

    passed: bool
    status: EvaluationStatus
    assertion_type: AssertionType
    expected: str
    reason: str


class TestResult(BaseModel):
    """Complete result produced after executing one AI test."""

    test_id: str
    name: str
    category: str
    prompt: str

    model: str
    actual_response: str

    status: EvaluationStatus
    passed: bool
    assertion_type: AssertionType
    expected: str
    reason: str

    response_time_seconds: float = Field(ge=0)
    prompt_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)

    executed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )