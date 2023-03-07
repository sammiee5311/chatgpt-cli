import pprint

from modules.chatgpt import ChatGPT
from utils.model import ChatGPTModel


def single_mode(chatgpt: ChatGPT) -> None:
    question = input("Question: ")
    response_text = chatgpt.ask(question)

    pprint.pprint(response_text)


def continuous_mode(chatgpt: ChatGPT) -> None:
    while True:
        question = input("Question: ")

        if question == "exit":
            break

        response_text = chatgpt.ask(question)
        pprint.pprint(response_text)


def start_asking(model: ChatGPTModel, continuous: bool) -> None:
    chatgpt = ChatGPT(model)

    if continuous:
        continuous_mode(chatgpt)
    else:
        single_mode(chatgpt)
