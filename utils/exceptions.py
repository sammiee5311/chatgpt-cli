from __future__ import annotations


class ChatGPTExecption(Exception):
    def __init__(
        self,
        detail: str = "Something went wrong via ChatGPT.",
    ) -> None:
        self.detail = detail

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name} - detail={self.detail!r}"
