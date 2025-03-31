from datetime import datetime, timezone, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from app.core.settings import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def create_jwt(self, data: dict) -> str:
        """Создаёт JWT-токен с указанными данными."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )