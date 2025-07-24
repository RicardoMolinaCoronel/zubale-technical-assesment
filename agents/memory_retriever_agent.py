from app.db import get_history_for_user
from langchain_core.messages import HumanMessage, AIMessage

class MemoryRetrieverAgent:
    def __call__(self, state):
        user_id = state["user_id"]
        raw_pairs = get_history_for_user(user_id)

        history = []
        for q, a in raw_pairs:
            history.append(HumanMessage(content=q))
            history.append(AIMessage(content=a))

        return {**state, "history": history}
