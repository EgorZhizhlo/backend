import os
from typing import Annotated
from datetime import date as d
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    async_sessionmaker,
    create_async_engine,
    AsyncSession
)
from .config import create_database_url


database_url = create_database_url()
engine = create_async_engine(database_url)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

str_not_none = Annotated[str, mapped_column(nullable=False)]
str_not_none_uniq = Annotated[str, mapped_column(nullable=False, unique=True)]
int_pk = Annotated[int, mapped_column(primary_key=True)]
int_not_none = Annotated[int, mapped_column(nullable=False)]
date_not_none = Annotated[d, mapped_column(nullable=False)]
b_flag = Annotated[bool, mapped_column(default=False, nullable=False)]


class Base(AsyncAttrs, DeclarativeBase):
    id: Mapped[int_pk]


async def get_db():
    async with async_session_maker() as session:
        yield session
