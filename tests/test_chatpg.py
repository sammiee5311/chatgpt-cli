from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from functools import partial
from typing import Any

import mock
import pytest

from modules.chatgpt import ChatGPT
from utils.exceptions import ChatGPTExecption
from utils.model import Davinci
from utils.model import Turbo


@dataclass
class CompletionMockResponse:
    choices: list[dict[str, str | dict[str, str]]] = field(default_factory=list)


def completion_mock_response(**kwgs: dict[str, Any]) -> CompletionMockResponse:
    if kwgs.get("fail"):
        return CompletionMockResponse()

    return CompletionMockResponse(
        choices=[
            {"text": "I am good, how are you?", "message": {"role": "assistant", "content": "I am good, how are you?"}}
        ]
    )


@mock.patch("openai.Completion.create", completion_mock_response)
def test_ask_success_with_davinci_model() -> None:
    chatgpt = ChatGPT(Davinci())
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"


@mock.patch("openai.Completion.create", partial(completion_mock_response, fail=True))
def test_ask_fail_with_davinci_model() -> None:
    chatgpt = ChatGPT(Davinci())
    with pytest.raises(ChatGPTExecption):
        chatgpt.ask("Hello, How are you?")


@mock.patch("openai.ChatCompletion.create", completion_mock_response)
def test_ask_success_with_turbo_model() -> None:
    chatgpt = ChatGPT(Turbo())
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"


@mock.patch("openai.ChatCompletion.create", partial(completion_mock_response, fail=True))
def test_ask_fail_with_turbo_model() -> None:
    chatgpt = ChatGPT(Turbo())
    with pytest.raises(ChatGPTExecption):
        chatgpt.ask("Hello, How are you?")
