import json

import pytest
from pydantic import ValidationError

from src.prompt_loader import load_prompt_tests


def test_load_valid_prompts(tmp_path):
    file_path = tmp_path / "prompts.json"
    file_path.write_text(
        json.dumps([
            {
                "id": "FUNC-001",
                "name": "Python creator",
                "category": "functional",
                "prompt": "Who created Python?",
                "assertion": {
                    "type": "contains",
                    "expected": "Guido van Rossum"
                }
            }
        ]),
        encoding="utf-8",
    )

    tests = load_prompt_tests(file_path)

    assert len(tests) == 1
    assert tests[0].id == "FUNC-001"


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        load_prompt_tests("missing.json")


def test_invalid_prompt_data(tmp_path):
    file_path = tmp_path / "prompts.json"
    file_path.write_text(
        '[{"id": "", "name": "Bad test"}]',
        encoding="utf-8",
    )

    with pytest.raises(ValidationError):
        load_prompt_tests(file_path)