from fastapi import APIRouter, Request, HTTPException, Depends, Response, Cookie
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from core import create_token, TOKEN_EXPIRATION, get_db, generate_random_data, verify_token
from app import Session, Params
from sqlalchemy.ext.asyncio import AsyncSession


session_router = APIRouter()


@session_router.post('/create')
async def create_session(
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    data = generate_random_data()
    uuid = generate_random_data()

    new_params = Params(
        font="Arial",
        font_color="#000000",
        font_size=20,
        logo="https://example.com/logo.png",
        bg_color="#FFFFFF",
        reply_color="#00FF00",
        request_color="#FF0000"
    )

    new_session = Session(
        token=data,
        uuid=uuid,
        params=new_params
    )

    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)

    new_token = create_token(data)
    response.set_cookie(key="auth_token", value=new_token,
                        httponly=True, max_age=TOKEN_EXPIRATION)
    return {"message": "Token generated and saved to cookie", "token": new_token}


@session_router.get('/get_uuid')
async def get_uuid(
    auth_token: str = Cookie(None),
    db: AsyncSession = Depends(get_db),
):

    if not auth_token:
        raise HTTPException(
            status_code=400, detail="Token is required in the cookie")

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

    return db_session.uuid
