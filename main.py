from fastapi import FastAPI
from fastapi import HTTPException
from app.schema import QueryInput
from graph.product_query_graph import rag_app
from dotenv import load_dotenv
app = FastAPI()

@app.post("/query")
def handle_query(input: QueryInput):
    validate_input(input)
    return rag_app.invoke({"query": input.query, "user_id": input.user_id})

def validate_input(input: QueryInput):
    if not input.user_id.strip() or not input.query.strip():
        raise HTTPException(status_code=400, detail="Both user_id and query must be non-empty strings.")
