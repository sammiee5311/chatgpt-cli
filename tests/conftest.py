import os
from pathlib import Path

import pytest

from modules.history import Database
from modules.history import History

DB_FILE = os.environ.get("DB_FILE", "./tests/history.sqlite3")


@pytest.fixture(scope="function")
def history_model() -> History:
    db_file = Path(DB_FILE)
    history = History(Database)

    history.save_messages("test", [{"role": "system", "content": "It is a test."}])
    yield history
    db_file.unlink()
