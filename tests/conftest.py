import os
from pathlib import Path
from typing import Generator
from typing import TypeVar

import pytest

from modules.history import Database
from modules.history import History

T = TypeVar("T")

YieldFixture = Generator[T, None, None]


DB_FILE = os.environ.get("DB_FILE", "./tests/history.sqlite3")


@pytest.fixture(scope="function")
def history_model() -> YieldFixture[History]:
    db_file = Path(DB_FILE)
    history = History(Database)

    history.save_messages("test", [{"role": "system", "content": "It is a test."}])
    yield history
    db_file.unlink()
