from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Any

import mock

from modules.chatgpt import ChatGPT
from utils.model import Davinci


@dataclass
class CompletionMockResponse:
    choices: list[dict[str, str]] = field(default_factory=list)


def completion_mock_response(**kwgs: dict[str, Any]) -> CompletionMockResponse:
    return CompletionMockResponse(choices=[{"text": "I am good, how are you?"}])


@mock.patch("openai.Completion.create", completion_mock_response)
def test_ask() -> None:
    chatgpt = ChatGPT(Davinci())
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"
