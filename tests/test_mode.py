import mock
import pytest
from pytest import CaptureFixture

from mode import single_mode
from modules.chatgpt import ChatGPT
from tests.test_chatgpt import completion_mock_response
from utils.model import Davinci


@mock.patch("openai.Completion.create", completion_mock_response)
def test_single_mode(capsys: CaptureFixture[str], fake_input: str) -> None:
    chatgpt = ChatGPT(Davinci())
    single_mode(chatgpt)

    captured = capsys.readouterr()
    response = completion_mock_response()

    assert f"'{response.choices[0]['text']}'\n" == captured.out
