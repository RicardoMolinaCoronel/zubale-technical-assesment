from langgraph.graph import StateGraph
from agents.retriever_agent import RetrieverAgent
from agents.responder_agent import ResponderAgent
from typing import TypedDict, List
from langchain_core.documents import Document

class RAGState(TypedDict):
    query: str
    user_id: str
    docs: List[Document]
    answer: str

retriever = RetrieverAgent()

responder = ResponderAgent()

graph = StateGraph(RAGState)
graph.add_node("Retriever", retriever)
graph.add_node("Responder", responder)

graph.set_entry_point("Retriever")
graph.add_edge("Retriever", "Responder")
graph.set_finish_point("Responder")

rag_app = graph.compile()
