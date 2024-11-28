import os
import secrets
import string
from fastapi import HTTPException
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    SALT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DB_PORT: str
    DB_HOST: str
    TOKEN_EXPIRATION: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


def create_database_url():
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")


SECRET_KEY = settings.SECRET_KEY.lower()
SALT = settings.SALT.lower()
TOKEN_EXPIRATION = settings.TOKEN_EXPIRATION

serializer = URLSafeTimedSerializer(SECRET_KEY)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def generate_random_data() -> str:
    length = 64
    """Generate a random string of fixed length."""
    characters = string.ascii_letters + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length)).lower()


def create_token(data):
    token = serializer.dumps(data, salt=SALT)
    return token


def verify_token(token):
    try:
        data = serializer.loads(
            token,
            salt=SALT,
            max_age=TOKEN_EXPIRATION
        )
        return data
    except SignatureExpired:
        raise HTTPException(status_code=400, detail="Token has expired")
    except BadSignature:
        raise HTTPException(status_code=400, detail="Invalid token")
