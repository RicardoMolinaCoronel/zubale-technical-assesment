from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()
print("🔑 Loaded API Key:", os.getenv("OPENAI_API_KEY"))  # Debug line
class ResponderAgent:
    def __init__(self):

        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3, openai_api_key=os.getenv("OPENAI_API_KEY"))

        self.prompt = PromptTemplate(
            input_variables=["context", "question"],
            template=(
        "You are a helpful and KINDLY assistant that ONLY answers using the provided context.\n"
        "Do not use any prior knowledge. If the answer is not explicitly stated in the context, reply:\n"
        "\"I don't know based on the provided information.\"\n\n"
        "Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
            )
        )
        self.output_parser = StrOutputParser()

    def format_context(self, docs):
        return "\n".join([doc.page_content for doc in docs])

    def respond(self, docs, query):
        context = self.format_context(docs)
        chain = self.prompt | self.llm | self.output_parser
        return chain.invoke({"context": context, "question": query})

    def __call__(self, state):
        docs = state["docs"]
        query = state["query"]
        response = self.respond(docs, query)
        return {"query": query, "docs": docs, "answer": response}