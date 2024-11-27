import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from session_ import session_router
from llm_ import llm_router
from params_ import params_router
from core import BASE_DIR
from core import engine, Base


app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

app.mount(
    "/media",
    StaticFiles(directory=os.path.join(BASE_DIR, "media")),
    name="media"
)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown():
    await engine.dispose()


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
