import pytest
import sqlite3
from app.db import init_db

DB_PATH = "conversation.db"

def _clear_conversation_history(user_ids: list[str]):
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.executemany(
            "DELETE FROM conversation_history WHERE user_id = ?",
            [(uid,) for uid in user_ids]
        )

@pytest.fixture(scope="function")
def clean_test_user():
    """
    Initializes DB and returns a clean user_id for testing.
    """
    init_db()
    user_id = "test_user_memory"
    _clear_conversation_history([user_id])
    return user_id

@pytest.fixture(scope="function")
def clean_test_2_users():
    """
    Initializes DB and returns two clean user_ids for testing.
    """
    init_db()
    user_ids = ["test_user_1", "test_user_2"]
    _clear_conversation_history(user_ids)
    return tuple(user_ids)
