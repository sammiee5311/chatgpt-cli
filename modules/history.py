from __future__ import annotations

import os
import sqlite3
from sqlite3 import Cursor
from types import TracebackType
from typing import cast
from typing import Type

import orjson

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
        exc_type: Type[BaseException] | None = None,
        exc_inst: BaseException | None = None,
        exc_tb: TracebackType | None = None,
    ) -> None:
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
            logger.debug("commiting...")
        self.conn.close()


class History:
    def __init__(self, database: Type[Database]):
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
        logger.info(f"History table has been created.")

    def delete_messages(self, name: str, created_at: str) -> None:
        with self.database() as curr:
            curr.execute("DELETE FROM history WHERE name = ? AND created_at = ?;", (name, created_at))
        logger.info(f"{name} - {created_at} has been deleted.")

    def save_messages(self, name: str, messages: list[dict[str, str]]) -> None:
        with self.database() as curr:
            curr.execute("INSERT INTO history (name, messages) VALUES (?, ?);", (name, orjson.dumps(messages)))
        logger.info(f"{name} has been saved.")

    def get_single_messages(self, name: str, created_at: str | None = None) -> list[dict[str, str]]:
        with self.database() as curr:
            if created_at:
                curr.execute("SELECT messages FROM history WHERE name = ? AND created_at = ?;", (name, created_at))
            else:
                curr.execute("SELECT messages FROM history WHERE name = ?;", (name,))

            messages = curr.fetchone()

        if not messages:
            raise Exception("Message does not exist.")

        return cast("list[dict[str, str]]", orjson.loads(messages[0]))

    def get_all_messages(self) -> list[tuple[str, str]]:
        with self.database() as curr:
            curr.execute("SELECT name, created_at FROM history;")
            fetched_messages = curr.fetchall()

        all_messages = [(name, created_at) for name, created_at in fetched_messages]

        return all_messages
