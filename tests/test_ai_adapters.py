"""Mocked tests for LLM adapters (no live network in CI)."""

from __future__ import annotations

import json
from unittest.mock import MagicMock, patch

from astrosim.ai.adapters import GrokLLMClient, OpenAILLMClient, _extract_completion


def test_extract_completion_parses_message():
    data = {"choices": [{"message": {"content": "  hello  "}}]}
    assert _extract_completion(data) == "hello"


def test_grok_offline_without_api_key():
    client = GrokLLMClient(api_key=None)
    result = client.complete("summarize mission")
    assert "offline" in result.lower()


@patch("astrosim.ai.adapters._post_json")
def test_grok_success(mock_post):
    mock_post.return_value = {"choices": [{"message": {"content": "Mission looks stable."}}]}
    client = GrokLLMClient(api_key="test-key")
    assert client.complete("prompt") == "Mission looks stable."


@patch("astrosim.ai.adapters._post_json", side_effect=TimeoutError("timeout"))
def test_grok_http_error_fallback(mock_post):
    client = GrokLLMClient(api_key="test-key")
    result = client.complete("prompt")
    assert "fallback" in result.lower()


def test_openai_offline_without_api_key():
    client = OpenAILLMClient(api_key=None)
    result = client.complete("summarize")
    assert "offline" in result.lower()


@patch("astrosim.ai.adapters._post_json")
def test_openai_empty_response_fallback(mock_post):
    mock_post.return_value = {"choices": []}
    client = OpenAILLMClient(api_key="key")
    result = client.complete("prompt")
    assert "fallback" in result.lower()


def test_llm_insight_schema_shape():
    from pathlib import Path

    import jsonschema

    schema = json.loads(
        (Path(__file__).resolve().parent.parent / "contracts" / "llm_insight.schema.json").read_text()
    )
    payload = {"content": "Stable energy margin.", "offline": True, "provider": "grok"}
    jsonschema.validate(payload, schema)