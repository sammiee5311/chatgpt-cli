from pathlib import Path
from typing import TypedDict

import openai

from modules.models import WhisperModels
from utils.exceptions import WhisperException

SUPPORTED_FILE_TYPES = frozenset([".mp3", ".mp4", ".mpeg", ".mpga", ".m4a", ".wav", ".webm"])
LIMIT_FILE_SIZE = 26_214_400  # < 25MB


class WhisperResult(TypedDict):
    text: str


class Voice:
    def __init__(self, model: WhisperModels):
        self.model = model

    def is_supported_audio_file_type(self, audio_file: Path) -> bool:
        return audio_file.suffix in SUPPORTED_FILE_TYPES

    def is_audio_file_samll_enough(self, audio_file: Path) -> bool:
        return audio_file.stat().st_size < LIMIT_FILE_SIZE

    def sanitize_audio_file(self, audio: str) -> Path:
        audio_file = Path(audio)

        if not audio_file.is_file():
            raise WhisperException(f"Audio is not a file.")
        if not self.is_supported_audio_file_type(audio_file):
            raise WhisperException(f"The file type of audio does not support. (support types: {SUPPORTED_FILE_TYPES})")
        if not self.is_audio_file_samll_enough(audio_file):
            raise WhisperException(f"Audio file is too big. (limit file size: {LIMIT_FILE_SIZE})")

        return audio_file

    def get_text_from_audio(self, audio: str) -> str:
        audio_file = self.sanitize_audio_file(audio)

        result: WhisperResult = openai.Audio.transcribe(str(self.model), audio_file.open("rb"))  # type:ignore

        if not result or "text" not in result:
            raise WhisperException()

        return result["text"]
