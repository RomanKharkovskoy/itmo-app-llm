import asyncio
from response import ResponseAgent
from search import SearchAgent
from parser import parse_to_json


def get_result(query):
    search_agent = SearchAgent()
    context = asyncio.run(search_agent.search(query))

    response_agent = ResponseAgent()
    result = asyncio.run(response_agent.generate_response(
        question=query, context=context))

    return parse_to_json(result)
