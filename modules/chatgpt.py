from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict
from typing import Union

import openai
from dotenv import load_dotenv

from utils.exceptions import ChatGPTExecption
from utils.model import ChatGPTModel

load_dotenv(dotenv_path=".env")

OPENAPI_KEY = os.environ.get("OPENAPI_KEY")
openai.api_key = OPENAPI_KEY

if not OPENAPI_KEY:
    raise ChatGPTExecption("Please set the 'OPENAPI_KEY' environment in '.env' file.")


@dataclass
class Choice(Dict[str, Union[str, int]]):
    finished_reason: str
    index: int
    text: str
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
    def __init__(self, model: ChatGPTModel) -> None:
        self.model = model

    def ask(self, text: str) -> str:
        response: ChatGPTResponse = openai.Completion.create(  # type: ignore
            engine=self.model.name,
            prompt=text,
            max_tokens=self.model.token,
            temperature=0.5,
        )

        if not response.choices:
            raise ChatGPTExecption("Open AI did not respond output from your prompt text. Please try again.")

        choice = response.choices[0]

        if not choice or not "text" in choice:
            raise ChatGPTExecption("Something went wrong.")

        if "text" in choice and isinstance(choice["text"], str):
            response_text = choice["text"].strip()

        return response_text
