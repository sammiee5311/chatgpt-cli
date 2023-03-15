from __future__ import annotations

import pytest

from modules.history import History


def test_create_history(history_model: History) -> None:
    all_messages = history_model.get_all_messages()

    assert len(all_messages) == 1
    assert all_messages[0][0] == "test"


def test_save_messages(history_model: History) -> None:
    messages = [{"role": "system", "content": "It is a test."}]
    history_model.save_messages("test2", messages)

    fetched_messages = history_model.get_single_messages("test2")

    assert fetched_messages == messages


def test_save_messages_not_exist(history_model: History) -> None:
    with pytest.raises(Exception):
        history_model.get_single_messages("test2")


def test_create_history(history_model: History) -> None:
    fetched_messages = history_model.get_all_messages()
    created_at = fetched_messages[0][1]
    history_model.delete_messages("test", created_at)

    all_messages = history_model.get_all_messages()

    assert len(all_messages) == 0
