from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from functools import partial
from typing import Any

import mock
import pytest

from modules.chatgpt import ChatGPT
from modules.models import ChatGPTModels
from modules.models import WhisperModels
from modules.voice import Voice
from utils.exceptions import ChatGPTExecption


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


def play_mock() -> None:
    ...


@mock.patch("openai.Completion.create", completion_mock_response)
def test_ask_success_with_davinci_model() -> None:
    chatgpt = ChatGPT(ChatGPTModels.DAVINCI.value())
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"


@mock.patch("openai.Completion.create", partial(completion_mock_response, fail=True))
def test_ask_fail_with_davinci_model() -> None:
    chatgpt = ChatGPT(ChatGPTModels.DAVINCI.value())
    with pytest.raises(ChatGPTExecption):
        chatgpt.ask("Hello, How are you?")


@mock.patch("openai.ChatCompletion.create", completion_mock_response)
def test_ask_success_with_turbo_model() -> None:
    chatgpt = ChatGPT(ChatGPTModels.TURBO.value())
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"


@mock.patch("openai.ChatCompletion.create", partial(completion_mock_response, fail=True))
def test_ask_fail_with_turbo_model() -> None:
    chatgpt = ChatGPT(ChatGPTModels.TURBO.value())
    with pytest.raises(ChatGPTExecption):
        chatgpt.ask("Hello, How are you?")


@mock.patch("modules.voice.Voice.play_voice_file", play_mock)
@mock.patch("openai.ChatCompletion.create", completion_mock_response)
def test_ask_with_turbo_model_and_enable_voice_assistant() -> None:
    chatgpt = ChatGPT(ChatGPTModels.TURBO.value(), Voice(WhisperModels.WHISPER1))
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"


@mock.patch("openai.ChatCompletion.create", completion_mock_response)
def test_ask_with_turbo_model_and_paid_version() -> None:
    chatgpt = ChatGPT(ChatGPTModels.TURBO.value(), paid=True)
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"


@mock.patch("modules.voice.Voice.play_voice_file", play_mock)
@mock.patch("openai.ChatCompletion.create", completion_mock_response)
def test_ask_with_turbo_model_and_paid_version_and_enable_voice_assistant() -> None:
    chatgpt = ChatGPT(ChatGPTModels.TURBO.value(), Voice(WhisperModels.WHISPER1), paid=True)
    response_text = chatgpt.ask("Hello, How are you?")

    assert response_text == "I am good, how are you?"
