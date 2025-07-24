from agents.retriever_agent import RetrieverAgent


# This test ensures that the RetrieverAgent indexes documents from the specified folder
# and successfully retrieves relevant documents based on a user query. This is a example for the product1.txt
def test_retrieve_documents():
    retriever = RetrieverAgent()
    query = "price of SmartSpeaker X200"
    retriever.index_documents_from_folder("documents")
    docs = retriever.retrieve(query)
    assert isinstance(docs, list)
    assert len(docs) > 0
    assert any("295" in doc.page_content.lower() for doc in docs)


