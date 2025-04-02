from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.services.yandex_api_service import YandexApiService
from app.core.db.db_repository import UserRepository
from app.core.db.session import get_db
from app.core.schemas.token import Token


class AuthService:
    def __init__(self, client: YandexApiService,  db: AsyncSession = Depends(get_db)):
        self.client = client
        self.db = db

    def _create_jwt(self, data: dict) -> str:
        """Создаёт JWT-токен с указанными данными."""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
    
    def decode_jwt(self, jwt_token: Token):
        try:
            payload = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            email = payload.get("sub")
            return email
        except JWTError:
            return "Invalid token"


    async def auth_with_yandex(self, code: str):
        access_token = await self.client.get_yandex_token(
            settings.TOKEN_URL,
            code,
            settings.YANDEX_CLIENT_ID,
            settings.YANDEX_CLIENT_SECRET
            )

        if not access_token:
            return None
        user_email = await self.client.get_user_email_by_yandex_token(
            settings.USER_INFO_URL,
            access_token
            )

        if not user_email:
            UserRepository.create_user(self.db, user_email)

        jwt_token = self._create_jwt({"sub": user_email})
        return Token(access_token=jwt_token, token_type="bearer")
