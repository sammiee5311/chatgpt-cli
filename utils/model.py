from dataclasses import dataclass
from enum import Enum
from typing import Protocol


@dataclass
class ChatGPTModel(Protocol):
    name: str
    token: int


@dataclass
class Davinci:
    name: str = "text-davinci-003"
    token: int = 4000


@dataclass
class Curie:
    name: str = "text-curie-001"
    token: int = 2048


@dataclass
class Babbage:
    name: str = "text-babbage-001"
    token: int = 2048


@dataclass
class Ada:
    name: str = "text-ada-001"
    token: int = 2048


class ChatGPTModels(Enum):
    DAVINCI = Davinci
    CURIE = Curie
    BABBAGE = Babbage
    ADA = Ada
