from __future__ import annotations

from argparse import ArgumentParser

from mode import start_asking
from utils.model import ChatGPTModel
from utils.model import ChatGPTModels

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
        "--paid",
        dest="paid",
        action="store_true",
        help="Use paid version.",
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
    paid: bool = args.paid

    print(
        f"You choose {model} model, {'continuous mode' if continuous else 'single mode'} and {'paid version' if paid else 'free version'}."
    )

    start_asking(model, continuous, paid)


if __name__ == "__main__":
    main()
