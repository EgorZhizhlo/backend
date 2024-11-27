import os
from core import BASE_DIR
from fastapi import (
    APIRouter, Request, File,
    UploadFile, Cookie, HTTPException, Depends
)
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.utils import secure_filename
from app import Session, Files
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from core import get_db, verify_token


llm_router = APIRouter()


@llm_router.post('/load_file')
async def load_and_ind_file(
    auth_token: str = Cookie(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    if file.size > 100 * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail="File size exceeds the limit of 10 MB")

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

    session_id = db_session.id

    media_dir = os.path.join(BASE_DIR, "media")
    safe_filename = secure_filename(file.filename)
    file_extension = os.path.splitext(safe_filename)[1]
    file_location = os.path.join(media_dir, f"{db_session.uuid}{file_extension}")

    try:
        with open(file_location, "wb") as f:
            content = await file.read()
            new_file = Files(
                session_id=session_id,
                file=f"media/{db_session.uuid}{file_extension}",
                text=content
            )
            db.add(new_file)
            await db.commit()
            await db.refresh(new_file)
            f.write(content)

    except Exception:
        raise HTTPException(status_code=500, detail="File upload failed")

    return {"filepath": f"media/{db_session.uuid}{file_extension}"}


@llm_router.post('/request')
async def request_to_llm():
    return {}
