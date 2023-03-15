import json
import os
import sqlite3
from sqlite3 import Cursor
from types import TracebackType
from typing import Optional
from typing import Type

from utils.log import logger

DB_FILE = os.environ.get("DB_FILE", "history.sqlite3")


class Database:
    def __init__(self, file: str = DB_FILE):
        self.file = file

    def __enter__(self) -> Cursor:
        self.conn = sqlite3.connect(self.file)
        return self.conn.cursor()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_inst: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> bool:
        logger.debug("commiting...")
        self.conn.commit()
        self.conn.close()


class History:
    def __init__(self, database: Database):
        self.database = database
        self.init_history()

    def init_history(self) -> None:
        if not self.has_history_table():
            self.create_table_for_messages()

    def has_history_table(self) -> bool:
        with self.database() as curr:
            curr.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history';")
            table = curr.fetchone()

        return table is not None

    def create_table_for_messages(self) -> None:
        with self.database() as curr:
            curr.execute(
                "CREATE TABLE history (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR(255), messages BLOB, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);"
            )

    def delete_messages(self, name: str, created_at) -> None:
        with self.database() as curr:
            curr.execute("DELETE FROM history WHERE name = ? AND created_at = ?;", (name, created_at))

    def save_messages(self, name: str, messages: list[dict[str, str]]) -> None:
        with self.database() as curr:
            curr.execute("INSERT INTO history (name, messages) VALUES (?, ?);", (name, json.dumps(messages)))

    def get_single_messages(self, name: str, created_at: str | None = None) -> list[dict[str, str]]:
        with self.database() as curr:
            if created_at:
                curr.execute("SELECT messages FROM history WHERE name = ? AND created_at = ?;", (name, created_at))
            else:
                curr.execute("SELECT messages FROM history WHERE name = ?;", (name,))

            messages = curr.fetchone()

        if not messages:
            raise Exception("Message does not exist.")

        return json.loads(messages[0])

    def get_all_messages(self):
        with self.database() as curr:
            curr.execute("SELECT name, created_at FROM history;")
            fetched_messages = curr.fetchall()

        all_messages = [(name, created_at) for name, created_at in fetched_messages]

        return all_messages
