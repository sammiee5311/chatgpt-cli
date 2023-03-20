from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict
from typing import Union

import openai
from dotenv import load_dotenv

from modules.models import ChatGPTModel
from modules.models import Turbo
from utils.exceptions import ChatGPTExecption

load_dotenv(dotenv_path=".env")

OPENAPI_KEY = os.environ.get("OPENAPI_KEY")
openai.api_key = OPENAPI_KEY

if not OPENAPI_KEY:
    raise ChatGPTExecption("Please set the 'OPENAPI_KEY' environment in '.env' file.")


@dataclass
class Message(Dict[str, str]):
    content: str
    role: str


@dataclass
class Choice(Dict[str, Union[str, int]]):
    finished_reason: str
    index: int
    text: str | None
    message: Message | None
    # logprobs: int | None ?


@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


@dataclass
class ChatGPTResponse:
    choices: list[Choice]
    created: int
    id: str
    model: str
    object: str
    usage: Usage


class ChatGPT:
    def __init__(self, model: ChatGPTModel, paid: bool = False) -> None:
        self.model = model
        self.is_paid = paid
        self.check_turbo_model()

    def check_turbo_model(self) -> None:
        self.is_turbo = self.model.__class__.__name__ == Turbo.__name__

        if self.is_turbo:
            self.reset_messages()

    def reset_messages(self) -> None:
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def set_messages(self, messages: list[dict[str, str]]) -> None:
        self.messages = messages

    def get_messages(self) -> list[dict[str, str]]:
        return self.messages

    def parse_choice_from_response(self, response: ChatGPTResponse) -> Choice:
        if not response.choices:
            raise ChatGPTExecption("Open AI did not respond output from your question. Please try again.")

        return response.choices[0]

    def sanitize_message_from_choice(self, choice: Choice) -> str:
        if not choice and not "message" in choice:
            raise ChatGPTExecption("Something went wrong.")

        if isinstance(choice["message"], dict) and isinstance(choice["message"]["content"], str):
            self.messages.append(choice["message"])
            response_text = choice["message"]["content"].strip()

        return response_text

    def send_question_with_turbo_model(self, text: str) -> str:
        if self.is_paid:
            self.reset_messages()

        self.messages.append({"role": "user", "content": text})

        response = openai.ChatCompletion.create(  # type: ignore
            model=self.model.name, messages=self.messages, max_tokens=self.model.token, temperature=0.5
        )

        choice = self.parse_choice_from_response(response)
        response_text = self.sanitize_message_from_choice(choice)

        return response_text

    def send_question_to_others_models(self, text: str) -> str:
        response = openai.Completion.create(  # type: ignore
            engine=self.model.name,
            prompt=text,
            max_tokens=self.model.token,
            temperature=0.5,
        )

        choice = self.parse_choice_from_response(response)

        if not choice and not "text" in choice:
            raise ChatGPTExecption("Something went wrong.")

        if "text" in choice and isinstance(choice["text"], str):
            response_text = choice["text"].strip()

        return response_text

    def ask(self, text: str) -> str:
        response_text = (
            self.send_question_with_turbo_model(text) if self.is_turbo else self.send_question_to_others_models(text)
        )

        return response_text
