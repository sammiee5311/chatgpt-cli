from __future__ import annotations

import os
from pathlib import Path
from typing import Generator
from typing import TypeVar

import mock
import pytest

from modules.history import Database
from modules.history import History

T = TypeVar("T")

YieldFixture = Generator[T, None, None]


DB_FILE = os.environ.get("DB_FILE", "./tests/history.sqlite3")
VOICE_FILE_WITH_MP3_SUFFIX = os.path.join("tests", "test.mp3")
BIG_SIZE_VOICE_FILE_WITH_MP4_SUFFIX = os.path.join("tests", "test.mp4")
VOICE_FILE_WITH_MP5_SUFFIX = os.path.join("tests", "test.mp5")
VOICE_NO_FILE = os.path.join("tests")


@pytest.fixture(scope="function")
def history_model() -> YieldFixture[History]:
    db_file = Path(DB_FILE)
    history = History(Database)

    history.save_messages("test", [{"role": "system", "content": "It is a test."}])
    yield history
    db_file.unlink()


@pytest.fixture(scope="function")
def voice_files() -> YieldFixture[dict[str, str]]:
    voice_file_with_mp3_suffix = Path(VOICE_FILE_WITH_MP3_SUFFIX)
    big_size_voice_file_with_mp4_suffix = Path(BIG_SIZE_VOICE_FILE_WITH_MP4_SUFFIX)
    voice_file_with_mp5_suffix = Path(VOICE_FILE_WITH_MP5_SUFFIX)
    voice_no_file = Path(VOICE_NO_FILE)

    voice_file_with_mp3_suffix.write_text("test")
    big_size_voice_file_with_mp4_suffix.write_text("bigtest")
    voice_file_with_mp5_suffix.write_text("test")

    yield {
        "mp3": str(voice_file_with_mp3_suffix),
        "big_size_mp4": str(big_size_voice_file_with_mp4_suffix),
        "mp5": str(voice_file_with_mp5_suffix),
        "no_file": str(voice_no_file),
    }
    voice_file_with_mp3_suffix.unlink()
    big_size_voice_file_with_mp4_suffix.unlink()
    voice_file_with_mp5_suffix.unlink()


@pytest.fixture
def fake_input(input_value: str = "test") -> YieldFixture[str]:
    with mock.patch("builtins.input"):
        yield input_value
