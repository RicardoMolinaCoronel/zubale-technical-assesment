from langgraph.graph import StateGraph
from agents.retriever_agent import RetrieverAgent
from agents.responder_agent import ResponderAgent
from agents.memory_retriever_agent import MemoryRetrieverAgent
from agents.memory_saver_agent import MemorySaverAgent
from typing import TypedDict, List
from typing import Annotated
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document
from langgraph.graph.message import add_messages
from app.db import init_db

init_db()

class RAGState(TypedDict):
    query: str
    user_id: str
    docs: List[Document]
    answer: str
    history: Annotated[List[BaseMessage], add_messages]


retriever = RetrieverAgent()
responder = ResponderAgent()

graph = StateGraph(RAGState)
graph.add_node("Retriever", retriever)
graph.add_node("Responder", responder)
graph.add_node("MemoryRetriever", MemoryRetrieverAgent())
graph.add_node("MemorySaver", MemorySaverAgent())

graph.set_entry_point("Retriever")
graph.add_edge("Retriever", "MemoryRetriever")
graph.add_edge("MemoryRetriever", "Responder")
graph.add_edge("Responder", "MemorySaver")
graph.set_finish_point("MemorySaver")


rag_app = graph.compile()

# Save the chart of the graph
'''
png_bytes = rag_app.get_graph().draw_mermaid_png()


with open("rag_graph.png", "wb") as f:
    f.write(png_bytes)

print("Graph chart stored on rag_graph.png")
'''