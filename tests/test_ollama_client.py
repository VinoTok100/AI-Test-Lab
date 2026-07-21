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
        "prompt_eval_duration": 100_000_000,
        "eval_duration": 400_000_000,
        "total_duration": 500_000_000,
        "load_duration": 20_000_000,
    }

    client = OllamaClient(
        model="llama3.1:latest",
        chat_function=mock_chat,
    )

    result = client.generate(
        "Who created the Python programming language?"
    )

    assert result.model == "llama3.1:latest"
    assert result.content == "Python was created by Guido van Rossum."

    assert result.prompt_tokens == 10
    assert result.response_time_seconds
    assert result.output_tokens == 8
    assert result.prompt_latency_seconds == 0.1
    assert result.generation_latency_seconds == 0.4

    assert result.prompt_tokens_per_second == 100.0
    assert result.generation_tokens_per_second == 20.0



    mock_chat.assert_called_once()