from __future__ import annotations

from io import BufferedReader
from pathlib import Path

import mock
import pytest

from modules.models import WhisperModels
from modules.voice import Voice
from modules.voice import WhisperResult
from utils.exceptions import WhisperException


def transcribe_mock_result(model: str, file: BufferedReader) -> WhisperResult:
    return WhisperResult(text="Hello")


def test_create_voice(voice_model: Voice) -> None:
    assert voice_model.model == WhisperModels.WHISPER1


@mock.patch("openai.Audio.transcribe", transcribe_mock_result)
def test_voice_file_success(voice_model: Voice, voice_files: dict[str, str]) -> None:
    result = voice_model.get_text_from_audio(voice_files["mp3"])

    assert result == "Hello"


@mock.patch("openai.Audio.transcribe", transcribe_mock_result)
def test_voice_file_fail(voice_model: Voice, voice_files: dict[str, str]) -> None:
    with pytest.raises(WhisperException):
        voice_model.get_text_from_audio(voice_files["mp5"])

    with pytest.raises(WhisperException):
        voice_model.get_text_from_audio(voice_files["no_file"])

    with pytest.raises(WhisperException):
        voice_model.get_text_from_audio(voice_files["big_size_mp4"])
