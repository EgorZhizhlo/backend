from fastapi import APIRouter, Request, HTTPException, Depends, Response
from core import create_token, TOKEN_EXPIRATION, get_db, generate_random_data
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
