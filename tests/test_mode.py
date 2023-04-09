import mock
import pytest
from pytest import CaptureFixture

from mode import Single
from modules.chatgpt import ChatGPT
from modules.models import Davinci
from tests.test_chatgpt import completion_mock_response


@pytest.mark.asyncio
@mock.patch("openai.Completion.create", completion_mock_response)
async def test_single_mode(capsys: CaptureFixture[str], fake_input: str) -> None:
    chatgpt = ChatGPT(Davinci())
    mode = Single(chatgpt)
    await mode.run()

    captured = capsys.readouterr()
    response = completion_mock_response()

    assert f"{response.choices[0]['text']}\n" == captured.out[-(len(response.choices[0]["text"]) + 1) :]
