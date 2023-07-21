from dataclasses import dataclass
from enum import Enum
from typing import Protocol


@dataclass
class ChatGPTModel(Protocol):
    name: str
    token: int

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class Turbo:
    name: str = "gpt-3.5-turbo"
    token: int = 4000

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class GPTFour:
    name: str = "gpt-4"
    token: int = 8192

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class GPTFour32K:
    name: str = "gpt-4-32k"
    token: int = 32768

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class Davinci:
    name: str = "text-davinci-003"
    token: int = 4000

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class Curie:
    name: str = "text-curie-001"
    token: int = 2048

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class Babbage:
    name: str = "text-babbage-001"
    token: int = 2048

    def __repr__(self) -> str:
        return self.__class__.__name__


@dataclass
class Ada:
    name: str = "text-ada-001"
    token: int = 2048

    def __repr__(self) -> str:
        return self.__class__.__name__


class ChatGPTModels(Enum):
    TURBO = Turbo
    DAVINCI = Davinci
    CURIE = Curie
    BABBAGE = Babbage
    ADA = Ada
    GPT_4 = GPTFour
    GPT_4_32K = GPTFour32K


class WhisperModels(Enum):
    WHISPER1 = "whisper-1"

    def __str__(self) -> str:
        return self.value
