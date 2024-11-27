from pydantic import BaseModel
from typing import Optional


class ParamsBase(BaseModel):
    font: Optional[str]
    font_color: Optional[str]
    logo: Optional[str]
    bg_color: Optional[str]
    reply_color: Optional[str]
    request_color: Optional[str]


class ParamsCreate(ParamsBase):
    pass


class ParamsSchema(ParamsBase):
    id: int

    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    token: str
    params_id: Optional[int]


class SessionCreate(SessionBase):
    pass


class SessionSchema(SessionBase):
    id: int
    params: Optional[ParamsSchema]

    class Config:
        orm_mode = True


class FilesBase(BaseModel):
    session_id: int
    file: Optional[str]
    text: Optional[bytes]


class FilesCreate(FilesBase):
    pass


class FilesSchema(FilesBase):
    id: int
    session: SessionSchema

    class Config:
        orm_mode = True
