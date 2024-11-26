from fastapi import APIRouter, Request


params_router = APIRouter()


@params_router.get('/get')
async def get_params():
    return {}


@params_router.put('/change')
async def change_params():
    return {}
