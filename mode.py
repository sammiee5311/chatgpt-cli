from __future__ import annotations

import pprint
import sys
from typing import Callable

from modules.chatgpt import ChatGPT
from modules.history import History
from utils.exceptions import InputException


class Single:
    def __init__(self, chatgpt: ChatGPT) -> None:
        self.chatgpt = chatgpt

    def run(self) -> None:
        question = input("Question: ")
        response_text = self.chatgpt.ask(question)
        pprint.pprint(response_text)


class Continuous:
    def __init__(self, chatgpt: ChatGPT) -> None:
        self.chatgpt = chatgpt

    def run(self) -> None:
        while True:
            question = input("Question: ")
            if question == "exit":
                break

            response_text = self.chatgpt.ask(question)
            pprint.pprint(response_text)


class ContinuousWithHistory:
    def __init__(self, chatgpt: ChatGPT, history: History):
        self.chatgpt = chatgpt
        self.history = history
        self.init_turbo()

    def init_turbo(self) -> None:
        options = {"1": self.delete_history, "2": self.activate_history, "0": lambda: sys.exit()}
        print("## Choose option ##\nDelete history [1]\nStart asking [2]\nExit [0]")
        idx = self.get_input("choose: ", lambda x: int(x) in range(3))
        options[idx]()

    def run(self) -> None:
        while True:
            question = input("Question: ")
            if question == "exit":
                self.process_save_history(self.chatgpt.get_messages())
                break

            response_text = self.chatgpt.ask(question)
            pprint.pprint(response_text)

    def get_input(
        self,
        prompt: str,
        validator: Callable[[str], bool],
        error_message: str = "Please, choose correct number which is one of the numbers next to data.",
    ) -> str:
        input_data = input(prompt)
        try:
            if not validator(input_data):
                raise InputException()
            return input_data
        except InputException:
            print(error_message)
            return self.get_input(prompt, validator)

    def activate_history(self) -> None:
        all_messages = self.history.get_all_messages()

        if len(all_messages) > 0:
            print("### START ASKING ###")
            self.show_all_messages(all_messages)

            idx = self.get_input("choose: ", lambda x: x.isdigit() and int(x) in range(len(all_messages) + 1))

            if idx != "0":
                name, created_at = all_messages[int(idx) - 1]
                messages = self.history.get_single_messages(name, created_at)
                self.chatgpt.set_messages(messages)

    def process_save_history(self, messages: list[dict[str, str]]) -> None:
        answer = input("Do you want to save message history? [y/n]")
        if answer == "y":
            name = self.get_input("Choose name of the history: ", lambda x: len(x.strip()) > 0, "Name cannot be empty.")
            self.history.save_messages(name, messages)

    def show_all_messages(self, all_messages: list[tuple[str, str]]) -> None:
        print("## Choose history ##")
        for idx, (name, created_at) in enumerate(all_messages):
            print(f"{name} - {created_at} [{idx+1}]")
        print("I don't want to choose [0]")

    def delete_history(self) -> None:
        print("##### DELETION #####")
        all_messages = self.history.get_all_messages()
        self.show_all_messages(all_messages)

        idx = self.get_input("choose: ", lambda x: x.isdigit() and int(x) in range(len(all_messages) + 1))

        if idx != "0":
            name, created_at = all_messages[int(idx) - 1]
            self.history.delete_messages(name, created_at)
