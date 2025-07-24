import sqlite3
from typing import List, Tuple

def get_db_connection():
    conn = sqlite3.connect("conversation.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS conversation_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            query TEXT NOT NULL,
            answer TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def get_history_for_user(user_id: str) -> List[Tuple[str, str]]:
    conn = get_db_connection()
    rows = conn.execute('''
        SELECT query, answer FROM conversation_history
        WHERE user_id = ?
        ORDER BY timestamp
    ''', (user_id,)).fetchall()
    conn.close()
    return [(r["query"], r["answer"]) for r in rows]

def save_to_history(user_id: str, query: str, answer: str):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO conversation_history (user_id, query, answer)
        VALUES (?, ?, ?)
    ''', (user_id, query, answer))
    conn.commit()
    conn.close()
