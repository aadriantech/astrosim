"""LLM provider adapters with graceful offline fallback."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


def _post_json(url: str, headers: dict[str, str], payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def _extract_completion(data: dict[str, Any]) -> str:
    choices = data.get("choices") or []
    if not choices:
        return ""
    message = choices[0].get("message") or {}
    return str(message.get("content", "")).strip()


def _resolve_grok_api_key() -> str | None:
    key = os.environ.get("XAI_API_KEY")
    if key:
        return key

    auth_paths = [
        Path.home() / ".config" / "grok" / "credentials",
        Path.home() / ".grok" / "credentials",
    ]
    for path in auth_paths:
        if not path.is_file():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                name, value = line.split("=", 1)
                if name.strip().lower() in {"xai_api_key", "api_key", "token"}:
                    return value.strip().strip('"').strip("'")
            else:
                return line
    return None


@dataclass
class GrokLLMClient:
    """xAI Grok chat-completions client with offline fallback."""

    model: str = "grok-2-latest"
    api_key: str | None = None
    base_url: str = "https://api.x.ai/v1/chat/completions"

    def __post_init__(self) -> None:
        if self.api_key is None:
            self.api_key = _resolve_grok_api_key()

    def complete(self, prompt: str) -> str:
        if not self.api_key:
            return (
                "[Grok offline] No XAI_API_KEY or grok credentials found. "
                "Returning heuristic summary instead."
            )

        try:
            data = _post_json(
                self.base_url,
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
            )
            content = _extract_completion(data)
            if content:
                return content
            return "[Grok fallback] Empty response from API."
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            return (
                "[Grok fallback] API request failed; using offline heuristic summary."
            )


@dataclass
class OpenAILLMClient:
    """OpenAI chat-completions client with offline fallback."""

    model: str = "gpt-4o-mini"
    api_key: str | None = None
    base_url: str = "https://api.openai.com/v1/chat/completions"

    def __post_init__(self) -> None:
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY")

    def complete(self, prompt: str) -> str:
        if not self.api_key:
            return (
                "[OpenAI offline] No OPENAI_API_KEY found. "
                "Returning heuristic summary instead."
            )

        try:
            data = _post_json(
                self.base_url,
                {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                {
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.2,
                },
            )
            content = _extract_completion(data)
            if content:
                return content
            return "[OpenAI fallback] Empty response from API."
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError):
            return (
                "[OpenAI fallback] API request failed; using offline heuristic summary."
            )