from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

import mock
from fastapi import status
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


@dataclass
class CompletionMockResponse:
    choices: list[dict[str, str]] = field(default_factory=list)


def completion_mock_response(**kwgs: dict[str, Any]) -> CompletionMockResponse:
    return CompletionMockResponse(choices=[{"text": "test"}])


def test_root() -> None:
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"text": "This is backend for chatGPT.", "message": "success"}


@mock.patch("openai.Completion.create", completion_mock_response)
def test_ask() -> None:
    response = client.post("/ask", json=dict(text="How are you?"))

    assert response.json() == {"text": "test", "message": "success"}
