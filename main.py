from __future__ import annotations

from argparse import ArgumentParser

from mode import Continuous
from mode import ContinuousWithHistory
from mode import Single
from modules.chatgpt import ChatGPT
from modules.history import Database
from modules.history import History
from modules.models import ChatGPTModel
from modules.models import ChatGPTModels

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

    mode: Continuous | ContinuousWithHistory | Single
    chatgpt = ChatGPT(model, paid)

    if continuous:
        mode = ContinuousWithHistory(chatgpt, History(Database)) if chatgpt.is_turbo else Continuous(chatgpt)
    else:
        mode = Single(chatgpt)

    mode.run()


if __name__ == "__main__":
    main()
