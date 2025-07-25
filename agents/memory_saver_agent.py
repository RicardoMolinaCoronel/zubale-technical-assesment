from app.db import save_to_history

#Save the current answer for user_id
class MemorySaverAgent:
    def __call__(self, state):
        user_id = state["user_id"]
        query = state["query"]
        answer = state.get("answer", "")

        if answer:
            save_to_history(user_id, query, answer)

        return state
