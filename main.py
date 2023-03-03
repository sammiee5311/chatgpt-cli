from __future__ import annotations

import pprint

from modules.chatgpt import ChatGPT
from utils.model import Davinci


def main() -> None:
    model = Davinci()

    chatgpt = ChatGPT(model)
    response_text = chatgpt.ask("Hello, How are you?")

    pprint.pprint(response_text)


if __name__ == "__main__":
    main()
