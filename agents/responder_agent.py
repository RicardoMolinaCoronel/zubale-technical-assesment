from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

load_dotenv()
#print("Loaded API Key:", os.getenv("OPENAI_API_KEY"))  # Debug line
class ResponderAgent:
    def __init__(self):

        self.llm = ChatOpenAI(model_name=os.getenv("LLM_MODEL", "gpt-4-turbo"), temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

        self.prompt = PromptTemplate(
            input_variables=["context", "question", "history"],
            template=(
                "You are an AI assistant called ZUBALSISTANT developed by Ricardo Molina to help users with general product-related questions.\n"
                "Your purpose is to assist kindly, professionally, and clearly using only the information provided in the conversation history and the product context below.\n"
                "Always address the user politely and, if known, by their name. If their name is not mentioned, simply say 'you'.\n"
                "Do not use external knowledge. If the answer is not present in the context or conversation history, respond with:\n"
                "\"I'm sorry, I don't know based on the information provided.\"\n\n"
                "Conversation history between user and you(the assistant):\n"
                "{history}\n\n"
                "Relevant product documentation:\n"
                "{context}\n\n"
                "The user now asks:\n"
                "{question}\n\n"
                "Your answer:"
            )
        )
        self.output_parser = StrOutputParser()

    def format_context(self, docs):
        return "\n".join([doc.page_content for doc in docs])

    def format_history(self, history: list[BaseMessage]) -> str:
        lines = []
        for msg in history:
            if isinstance(msg, HumanMessage):
                role = "User"
            elif isinstance(msg, AIMessage):
                role = "Assistant"
            else:
                role = "Unknown"
            lines.append(f"{role}: {msg.content}")
        return "\n".join(lines)

    def respond(self, docs, query, history):
        context = self.format_context(docs)
        conversation = self.format_history(history)
        print(context)
        chain = self.prompt | self.llm | self.output_parser
        return chain.invoke({"context": context, "question": query, "history": conversation})

    def __call__(self, state):
        docs = state["docs"]
        query = state["query"]
        history = state.get("history", [])
        answer = self.respond(docs, query, history)
        history = history + [HumanMessage(content=query), AIMessage(content=answer)]
        return {"query": query, "docs": docs, "answer": answer, "history": history}