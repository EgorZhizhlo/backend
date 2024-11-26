from fastapi import APIRouter, Request


llm_router = APIRouter()


@llm_router.post('/load_file')
async def load_and_ind_file():
    return {}


@llm_router.post('/request')
async def request_to_llm():
    return {}
