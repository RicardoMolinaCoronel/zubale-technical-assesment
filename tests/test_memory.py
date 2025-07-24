import pytest
from graph.product_query_graph import rag_app
from app.db import get_history_for_user
import uuid

def test_memory_is_user_specific(clean_test_2_users):
    user1, user2 = clean_test_2_users

    # First interaction for every user
    res1 = rag_app.invoke({"query": "My name is Ricardo", "user_id": user1})
    res2 = rag_app.invoke({"query": "My name is Jaime", "user_id": user2})

    assert "answer" in res1
    assert "answer" in res2

    # Second interaction, asking their names
    res1_followup = rag_app.invoke({"query": "Say only my name", "user_id": user1})
    res2_followup = rag_app.invoke({"query": "Say only my name", "user_id": user2})

    assert "Ricardo" in res1_followup["answer"]
    assert "Jaime" in res2_followup["answer"]

    # Verifying separated histories
    hist1 = get_history_for_user(user1)
    hist2 = get_history_for_user(user2)

    assert len(hist1) >= 2
    assert len(hist2) >= 2

    for q, a in hist1:
        assert isinstance(q, str)
        assert isinstance(a, str)

    for q, a in hist2:
        assert isinstance(q, str)
        assert isinstance(a, str)

    # We confirm that the conversation is saved independently by user_id
    user1_last_question = hist1[-1][0].lower()
    user2_last_question = hist2[-1][0].lower()
    assert "say only my name" in user1_last_question
    assert "say only my name" in user2_last_question