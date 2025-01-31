from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from src.tools.response import ResponseAgent
from src.tools.search import SearchAgent
from src.utils.parser import parse_to_json

app = FastAPI()


def get_result(id, query):
    search_agent = SearchAgent()
    context = asyncio.run(search_agent.search(query))

    response_agent = ResponseAgent()
    result = asyncio.run(response_agent.generate_response(
        question=query, context=context))

    return parse_to_json(id, result)


class QueryRequest(BaseModel):
    query: str
    id: int


@app.post("/api/request")
def process_query(request: QueryRequest):
    query_text = request.query
    request_id = request.id
    try:
        response = get_result(id=request_id, query=query_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка: {e}")

    return response
