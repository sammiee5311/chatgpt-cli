from __future__ import annotations

import asyncio
import itertools
import os
from asyncio import create_task
from asyncio import get_event_loop
from dataclasses import dataclass
from functools import partial
from typing import Dict
from typing import Union

import openai
from dotenv import load_dotenv

from modules.models import ChatGPTModel
from modules.models import Turbo
from modules.voice import Voice
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


async def print_waiting_prompt() -> None:
    for char in itertools.cycle([r".", r"..", r"..."]):
        status = f"\rWaiting a response from ChatGPT{char}"
        print(status, flush=True, end="")
        try:
            await asyncio.sleep(0.5)
        except asyncio.CancelledError:
            break

    blanks = " " * len(status)
    print(f"\r{blanks}\r", end="")


class ChatGPT:
    def __init__(self, model: ChatGPTModel, voice: Voice | None = None, paid: bool = False) -> None:
        self.model = model
        self.is_paid = paid
        self.voice = voice
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

    async def send_question_with_turbo_model(self, text: str) -> str:
        if not self.is_paid:
            self.reset_messages()

        self.messages.append({"role": "user", "content": text})

        waiting_response = create_task(print_waiting_prompt())

        response = await openai.ChatCompletion.acreate(  # type:ignore
            model=self.model.name, messages=self.messages, max_tokens=self.model.token, temperature=0.5
        )

        waiting_response.cancel()

        choice = self.parse_choice_from_response(response)
        response_text = self.sanitize_message_from_choice(choice)

        return response_text

    async def send_question_with_others_models(self, text: str) -> str:
        waiting_response = create_task(print_waiting_prompt())

        response = await openai.Completion.acreate(  # type:ignore
            engine=self.model.name,
            prompt=text,
            max_tokens=self.model.token,
            temperature=0.5,
        )

        waiting_response.cancel()

        choice = self.parse_choice_from_response(response)

        if not choice and not "text" in choice:
            raise ChatGPTExecption("Something went wrong.")

        if "text" in choice and isinstance(choice["text"], str):
            response_text = choice["text"].strip()

        return response_text

    async def ask(self, text: str) -> str:
        response_text = await (
            self.send_question_with_turbo_model(text) if self.is_turbo else self.send_question_with_others_models(text)
        )

        if self.voice:
            self.voice.speak(response_text)

        return response_text
