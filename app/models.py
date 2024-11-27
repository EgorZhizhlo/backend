from sqlalchemy import Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.orm import Mapped
from core import (Base, str_not_none, int_not_none)


class Params(Base):
    __tablename__ = "params"

    font: Mapped[str_not_none]
    font_color: Mapped[str_not_none]
    font_size: Mapped[int_not_none]
    logo: Mapped[str_not_none]
    bg_color: Mapped[str_not_none]
    reply_color: Mapped[str_not_none]
    request_color: Mapped[str_not_none]

    sessions: Mapped["Session"] = relationship(
        "Session", back_populates="params")

    extend_existing = True


class Session(Base):
    __tablename__ = "session"

    token: Mapped[str_not_none]
    uuid: Mapped[str_not_none]
    params_id: Mapped[int] = mapped_column(ForeignKey("params.id"))

    params: Mapped[Params] = relationship("Params", back_populates="sessions")
    files: Mapped["Files"] = relationship(
        "Files", back_populates="session")

    extend_existing = True


class Files(Base):
    __tablename__ = "files"

    session_id: Mapped[int] = mapped_column(ForeignKey("session.id"))
    text: Mapped[bytes] = mapped_column(LargeBinary)

    session: Mapped[Session] = relationship("Session", back_populates="files")

    extend_existing = True
