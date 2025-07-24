
from agents.responder_agent import ResponderAgent
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage

# This test checks that the ResponderAgent correctly generates a response
# by using both the retrieved document context and the user conversation history.
def test_prompt_uses_context_and_history():
    agent = ResponderAgent()
    docs = [Document(page_content='''Product: SmartSpeaker X200
    Battery Life: Up to 15 hours
    Water Resistant: Yes (IPX4)
    Price: 295$
    Material: Premium aluminum body with silicone base
    Connectivity: Bluetooth 5.3 and Wi-Fi enabled''')]

    history = [
        HumanMessage(content="Hello"),
        AIMessage(content="Hi! How can I help?")
    ]
    query = "How long does the battery of the SmartSpeaker last?"

    response = agent.respond(docs, query, history)

    assert isinstance(response, str)
    assert "15 hours" in response




