from fastapi import APIRouter, Request, Depends, HTTPException, Cookie, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app import ParamsSchema, ParamsCreate, Params, Session
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from core import get_db, verify_token


params_router = APIRouter()


@params_router.get("/get", response_model=ParamsSchema)
async def get_params(
    uuid_token: str = Query(...),
    db: AsyncSession = Depends(get_db),
):

    if not uuid_token:
        raise HTTPException(
            status_code=400, detail="Token is required")

    result = await db.execute(
        select(Params)
        .join(Session)
        .where(Session.uuid == uuid_token)
        .options(selectinload(Params.sessions))
    )

    params = result.scalar_one_or_none()

    if not params:
        raise HTTPException(
            status_code=404, detail="Params not found for the provided token")

    return params


@params_router.put("/change", response_model=ParamsSchema)
async def update_params(
    params_update: ParamsCreate,
    auth_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):

    if not auth_token:
        raise HTTPException(
            status_code=400, detail="Token is required")

    enc_token = verify_token(auth_token)

    session_result = await db.execute(
        select(Session).options(selectinload(Session.params)).where(
            Session.token == enc_token)
    )
    db_session = session_result.scalar_one_or_none()

    if not db_session or not db_session.params:
        raise HTTPException(
            status_code=404,
            detail="Session or Params not found for the provided token")

    db_params = db_session.params
    for key, value in params_update.dict(exclude_unset=True).items():
        setattr(db_params, key, value)

    await db.commit()
    await db.refresh(db_params)

    return db_params
