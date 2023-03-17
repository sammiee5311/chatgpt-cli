from __future__ import annotations

import pprint

from modules.chatgpt import ChatGPT
from modules.history import Database
from modules.history import History
from utils.exceptions import InputException
from utils.model import ChatGPTModel


def show_all_messages(all_messages: list[tuple[str, str]]) -> None:
    print("## Choose saved data##")
    for idx, (name, created_at) in enumerate(all_messages):
        print(f"{name} - {created_at} [{idx+1}]")
    print("I don't want to choose [0]")


def sanitize_input_data(input_data: str, number_of_data: int) -> int:
    if not input_data.isdigit() or not (0 <= int(input_data) <= number_of_data):
        raise InputException()

    return int(input_data) - 1


def single_mode(chatgpt: ChatGPT) -> None:
    question = input("Question: ")
    response_text = chatgpt.ask(question)

    pprint.pprint(response_text)


def activate_history(chatgpt: ChatGPT) -> History:
    history = History(Database)
    all_messages = history.get_all_messages()

    if len(all_messages) > 0:
        show_all_messages(all_messages)
        while True:
            try:
                idx = sanitize_input_data(input("choose : "), len(all_messages))

                if idx == -1:
                    return history
                break
            except InputException:
                print("Please, choose correct number which is one of the numbers next to data.")

        name, created_at = all_messages[idx]
        messages = history.get_single_messages(name, created_at)
        chatgpt.set_messages(messages)

    return history


def process_save_history(history: History, messages: list[dict[str, str]]) -> None:
    answer = input("Do you want to save message history? [y/n]")

    if answer == "y":
        while True:
            name = input("Choose name of the history: ").strip()

            if len(name) < 1:
                print("Name of the history cannot be empty string.")
                continue
            break

        history.save_messages(name, messages)


def continuous_mode(chatgpt: ChatGPT) -> None:
    if chatgpt.is_turbo:
        history = activate_history(chatgpt)

    while True:
        question = input("Question: ")
        if question == "exit":
            if chatgpt.is_turbo:
                process_save_history(history, chatgpt.get_messages())
            break

        response_text = chatgpt.ask(question)
        pprint.pprint(response_text)


def start_asking(model: ChatGPTModel, continuous: bool) -> None:
    chatgpt = ChatGPT(model)

    if continuous:
        continuous_mode(chatgpt)
    else:
        single_mode(chatgpt)
