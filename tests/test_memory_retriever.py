import sqlite3
import pytest
from app.db import init_db, save_to_history, get_history_for_user
from agents.memory_retriever_agent import MemoryRetrieverAgent
from langchain_core.messages import HumanMessage, AIMessage


def test_get_history_for_user_returns_correct_pairs(clean_test_user):
    user_id = clean_test_user
    save_to_history(user_id, "What is your name?", "I'm an AI assistant.")
    save_to_history(user_id, "What do you do?", "I assist with product questions.")
    history = get_history_for_user(user_id)

    assert isinstance(history, list)
    assert len(history) == 2
    assert history[0] == ("What is your name?", "I'm an AI assistant.")
    assert history[1] == ("What do you do?", "I assist with product questions.")

def test_memory_retriever_agent_formats_messages(clean_test_user):
    user_id = clean_test_user
    save_to_history(user_id, "What is your name?", "I'm an AI assistant.")
    save_to_history(user_id, "What do you do?", "I assist with product questions.")
    agent = MemoryRetrieverAgent()
    state = {"user_id": user_id}
    updated_state = agent(state)
    history = updated_state.get("history")

    assert isinstance(history, list)
    assert len(history) == 4
    assert isinstance(history[0], HumanMessage)
    assert history[0].content == "What is your name?"
    assert isinstance(history[1], AIMessage)
    assert history[1].content == "I'm an AI assistant."
