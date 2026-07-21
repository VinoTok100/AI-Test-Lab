import pytest

from src.ollama_client import OllamaClient


@pytest.mark.integration
def test_real_llama_response():
    client = OllamaClient(model="llama3.1:latest")

    result = client.generate(
        "Who created the Python programming language? "
        "Answer in one short sentence."
    )

    assert result.model == "llama3.1:latest"
    assert "Guido" in result.content
    assert result.prompt_tokens > 0
    assert result.output_tokens > 0
    assert result.response_time_seconds > 0