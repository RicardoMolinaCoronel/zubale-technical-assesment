from fastapi import FastAPI
from app.schema import QueryInput
from graph.product_query_graph import rag_app
from dotenv import load_dotenv
app = FastAPI()


@app.post("/query")
def handle_query(input: QueryInput):
    result = rag_app.invoke({"query": input.query, "user_id": input.user_id})
    return result