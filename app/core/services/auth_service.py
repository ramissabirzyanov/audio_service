from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError

from app.core.settings import settings
from app.core.services.yandex_api_service import YandexApiClient
from app.core.services.user_service import UserService
from app.core.schemas.token import Token, AuthResponse



class AuthService:
    def __init__(self, client: YandexApiClient, user_service: UserService) -> AuthResponse:
        self.client = client
        self.user_service = user_service

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


    async def auth_with_yandex(self, code: str) -> AuthResponse:
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

        user = await self.user_service.get_or_create_user(user_email)  

        jwt_token = self._create_jwt({"sub": user_email})
        return AuthResponse(
            access_token=jwt_token,
            token_type="bearer",
            user_email=user.email
        )
