from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from funcs import get_result

app = FastAPI()


class QueryRequest(BaseModel):
    query: str
    id: int


@app.post("/api/request")
def process_query(request: QueryRequest):
    query_text = request.query
    request_id = request.id
    try:
        response = get_result(query=query_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка OpenAI: {e}")

    return response
