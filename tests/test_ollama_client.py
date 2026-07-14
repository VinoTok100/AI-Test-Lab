from unittest.mock import Mock

from src.ollama_client import OllamaClient


def test_generate_returns_model_response():
    mock_chat = Mock()
    mock_chat.return_value = {
        "model": "llama3.1:latest",
        "message": {
            "role": "assistant",
            "content": "Python was created by Guido van Rossum.",
        },
        "prompt_eval_count": 10,
        "eval_count": 8,
    }

    client = OllamaClient(
        model="llama3.1:latest",
        chat_function=mock_chat,
    )

    result = client.generate("Who created Python?")

    assert result.model == "llama3.1:latest"
    assert result.content == "Python was created by Guido van Rossum."
    assert result.prompt_tokens == 10
    assert result.output_tokens == 8
    assert result.response_time_seconds >= 0