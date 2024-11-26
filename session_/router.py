from fastapi import APIRouter, Request


session_router = APIRouter()


@session_router.post('/create')
async def create_session():
    return {}


@session_router.get('/get')
async def get_session():
    return {}
