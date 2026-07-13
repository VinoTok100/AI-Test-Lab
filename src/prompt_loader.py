import json
from pathlib import Path

from src.models import PromptTest


def load_prompt_tests(file_path: str | Path) -> list[PromptTest]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return [PromptTest.model_validate(item) for item in raw_data]