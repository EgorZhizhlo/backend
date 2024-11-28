import aiohttp
import tempfile
from fastapi import (
    APIRouter, File, Body,
    UploadFile, Cookie, HTTPException, Depends
)
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from app import Session, Files
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from core import get_db, verify_token
from .text_extractors import TextFileExtractor, TextUrlExtractor


llm_router = APIRouter()


async def add_request_to_llm(session_token: str, text: str):
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://app:8000/add-document',
            json={"session_token": session_token, "text": text}
        ) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail=await response.text()
                )
            return await response.json()


@llm_router.post('/load_file')
async def load_and_ind_file(
    auth_token: str = Cookie(None),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):

    if file.size > 100 * 1024 * 1024:
        raise HTTPException(
            status_code=400, detail="File size exceeds the limit of 100 MB")

    # Проверяем наличие токена
    if not auth_token:
        raise HTTPException(
            status_code=400, detail="Token is required in the cookie"
        )

    # Проверяем валидность токена
    enc_token = verify_token(auth_token)

    # Проверяем существование сессии и параметров
    session_result = await db.execute(
        select(Session).options(selectinload(Session.params)).where(
            Session.token == enc_token
        )
    )
    db_session = session_result.scalar_one_or_none()

    if not db_session or not db_session.params:
        raise HTTPException(
            status_code=404,
            detail="Session or Params not found for the provided token"
        )

    session_id = db_session.id

    try:
        original_filename = Path(file.filename)
        suffix = original_filename.suffix

        if suffix.lower() not in [".pdf", ".docx", ".txt"]:
            raise ValueError(f"Недопустимый формат файла: {suffix}")

        with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=suffix
        ) as temp_file:
            temp_file.write(await file.read())
            temp_file_path = Path(temp_file.name)

        content = TextFileExtractor.extract_text(str(temp_file_path))

        temp_file_path.unlink()

        new_file = Files(
            session_id=session_id,
            text=content.encode("utf-8")
        )

        await add_request_to_llm(str(session_id), content)
        db.add(new_file)
        await db.commit()
        await db.refresh(new_file)
    except ValueError as e:
        raise HTTPException(
            status_code=400, detail=f"Ошибка при обработке файла: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Ошибка при загрузке файла: {str(e)}"
        )

    return {"message": f"Файл '{original_filename.name}' успешно обработан и сохранен"}


@llm_router.post('/load_url')
async def load_and_ind_url(
    auth_token: str = Cookie(None),
    url: str = Body(...),
    db: AsyncSession = Depends(get_db),
):

    if not auth_token:
        raise HTTPException(
            status_code=400, detail="Token is required in the cookie"
        )

    enc_token = verify_token(auth_token)

    session_result = await db.execute(
        select(Session).options(selectinload(Session.params)).where(
            Session.token == enc_token
        )
    )
    db_session = session_result.scalar_one_or_none()

    if not db_session or not db_session.params:
        raise HTTPException(
            status_code=404,
            detail="Session or Params not found for the provided token"
        )

    session_id = db_session.id

    try:
        content = await TextUrlExtractor.extract_text(url)

        new_file = Files(
            session_id=session_id,
            text=content.encode("utf-8")
        )
        await add_request_to_llm(str(session_id), content)
        db.add(new_file)
        await db.commit()
        await db.refresh(new_file)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing URL: {str(e)}"
        )

    return {"message": f"Content from URL '{url}' successfully processed and saved"}


@llm_router.post('/request')
async def request_to_llm():
    return {}
