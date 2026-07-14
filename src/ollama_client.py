from collections.abc import Callable
from time import perf_counter
from typing import Any

from ollama import chat

from src.models import ModelResponse


class OllamaClient:
    """Client for sending prompts to a local Ollama model."""

    def __init__(
        self,
        model: str,
        chat_function: Callable[..., Any] = chat,
    ) -> None:
        self.model = model
        self._chat_function = chat_function

    def generate(self, prompt: str) -> ModelResponse:
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        started_at = perf_counter()

        response = self._chat_function(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        elapsed = perf_counter() - started_at

        return ModelResponse(
            model=response["model"],
            content=response["message"]["content"].strip(),
            response_time_seconds=elapsed,
            prompt_tokens=response.get("prompt_eval_count"),
            output_tokens=response.get("eval_count"),
        )