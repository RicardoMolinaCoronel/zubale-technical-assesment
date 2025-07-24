# tests/test_retriever.py
import os
import pytest
from agents.retriever_agent import RetrieverAgent



def test_retrieve_documents():
    retriever = RetrieverAgent()
    query = "price of SmartSpeaker X200"
    retriever.index_documents_from_folder("documents")
    docs = retriever.retrieve(query)
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert any("295" in doc.page_content.lower() for doc in docs)


