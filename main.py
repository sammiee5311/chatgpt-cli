from __future__ import annotations

import pprint
from argparse import ArgumentParser

from modules.chatgpt import ChatGPT
from utils.model import ChatGPTModel
from utils.model import ChatGPTModels

models = map(lambda name: name.lower(), ChatGPTModels._member_names_)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "-m",
        "--model",
        dest="model",
        default="davinci",
        choices=list(models),
        help=f"Please choose one of the {list(models)} models.",
    )
    args = parser.parse_args()

    model: ChatGPTModel = ChatGPTModels[args.model.upper()].value()

    chatgpt = ChatGPT(model)
    response_text = chatgpt.ask("Hello, How are you?")

    pprint.pprint(response_text)


if __name__ == "__main__":
    main()
