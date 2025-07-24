import os
import pytest
from graph.product_query_graph import rag_app
from app.db import get_history_for_user
from langchain_core.messages import HumanMessage, AIMessage

@pytest.fixture
def initial_state():
    return {
        "query": "How long does the SmartSpeaker X200 battery last?",
        "user_id": "test_user_123"
    }

def test_full_rag_flow(initial_state):
    result = rag_app.invoke(initial_state)

    # Verify response
    assert "answer" in result
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
    print(result["answer"])

    # Verify used docs
    assert "docs" in result
    assert isinstance(result["docs"], list)
    assert len(result["docs"]) > 0

    # Verify history updated
    assert "history" in result
    assert isinstance(result["history"], list)
    assert any(isinstance(m, HumanMessage) for m in result["history"])
    assert any(isinstance(m, AIMessage) for m in result["history"])

    # Verify data base persistance
    history_from_db = get_history_for_user("test_user_123")
    assert any("battery" in q.lower() for q, _ in history_from_db)
