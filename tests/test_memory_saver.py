
from app.db import get_history_for_user
from agents.memory_saver_agent import MemorySaverAgent


# This test verifies that MemorySaverAgent correctly persists a query-answer pair to the database
def test_memory_saver_agent_saves_interaction(clean_test_user):
    user_id = clean_test_user
    state = {
        "user_id": user_id,
        "query": "What is this device for?",
        "answer": "It is used to play music and connect to other devices."
    }

    agent = MemorySaverAgent()
    agent(state)
    history = get_history_for_user(user_id)
    assert len(history) == 1
    assert history[0][0] == state["query"]
    assert history[0][1] == state["answer"]

# This test ensures that MemorySaverAgent does not save an interaction if the answer is empty
def test_memory_saver_agent_does_not_save_empty_answer(clean_test_user):
    user_id = clean_test_user
    state = {
        "user_id": user_id,
        "query": "What is your name?",
        "answer": ""
    }
    agent = MemorySaverAgent()
    agent(state)
    history = get_history_for_user(user_id)
    assert len(history) == 0
