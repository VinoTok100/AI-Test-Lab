import pytest
from pydantic import ValidationError

from src.models import PromptTest


def test_valid_prompt_model():
    test_case = PromptTest(
        id="FUNC-001",
        name="Python creator",
        category="functional",
        prompt="Who created Python?",
        assertion={
            "type": "contains",
            "expected": "Guido van Rossum",
        },
    )

    assert test_case.id == "FUNC-001"
    assert test_case.assertion.expected == "Guido van Rossum"


def test_invalid_assertion_type():
    with pytest.raises(ValidationError):
        PromptTest(
            id="FUNC-002",
            name="Invalid assertion",
            category="functional",
            prompt="Who created Python?",
            assertion={
                "type": "contain",
                "expected": "Guido van Rossum",
            },
        )