from pydantic import BaseModel

class QueryInput(BaseModel):
    user_id: str
    query: str