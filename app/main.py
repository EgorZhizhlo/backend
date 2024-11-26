from fastapi import FastAPI
from session_ import session_router
from llm_ import llm_router
from params_ import params_router


app = FastAPI()

app.include_router(
    session_router,
    prefix="/session",
    tags=['Сессия']
)

app.include_router(
    llm_router,
    prefix="/llm",
    tags=['LLM']
)

app.include_router(
    params_router,
    prefix="/params",
    tags=['Параметры']
)
