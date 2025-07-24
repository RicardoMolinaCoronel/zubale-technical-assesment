from agents.responder_agent import ResponderAgent
from agents.retriever_agent import RetrieverAgent
import os
from dotenv import load_dotenv

# This test verifies that environment variables are correctly loaded and used
# to configure the RetrieverAgent and ResponderAgent with the expected settings.
def test_environment_variables():
    load_dotenv()
    os.environ["TOP_K"] = "5"
    os.environ["LLM_MODEL"] = "gpt-3.5-turbo"
    os.environ["EMBEDDING_MODEL"] = "all-MiniLM-L6-v2"
    retriever = RetrieverAgent()
    responder = ResponderAgent()

    assert retriever.k == 5
    assert retriever.embedder.model_name == "all-MiniLM-L6-v2"
    assert responder.llm.model_name == "gpt-3.5-turbo"