from __future__ import annotations

from argparse import ArgumentParser

from mode import start_asking
from utils.exceptions import ChatGPTExecption
from utils.model import ChatGPTModel
from utils.model import ChatGPTModels
from utils.model import Turbo

models = list(map(lambda name: name.lower(), ChatGPTModels._member_names_))


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--con",
        dest="continuous",
        action="store_true",
        help="Ask continuous questions to ChatGPT.",
    )
    parser.add_argument(
        "-m",
        "--model",
        dest="model",
        default="davinci",
        choices=models,
        help=f"Please choose one of the {models} models. (Default is 'Davinci' model)",
    )
    args = parser.parse_args()

    model: ChatGPTModel = ChatGPTModels[args.model.upper()].value()
    continuous: bool = args.continuous

    print(f"You choose {model} model and {'continuous mode' if continuous else 'single mode'}.")

    start_asking(model, continuous)


if __name__ == "__main__":
    main()
