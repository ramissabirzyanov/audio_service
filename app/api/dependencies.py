from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.settings import settings
from app.core.db.db_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.models.user import User
from app.core.services.yandex_api_service import YandexApiClient
from app.core.services.auth_service import AuthService
from app.core.services.user_service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    db: AsyncSession,
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return {"error": "Could not validate data"}

    email = payload.get("sub")

    if email is None:
        return {"error": "Invalid data"}

    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email)
    if user is None:
        return {"error": "User not found"}

    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        return {
            "error": "PermissionError",
            "message": f"You don't have rights!"
        }
    return current_user


def get_auth_service(yandex_client: YandexApiClient = Depends()) -> AuthService:
    return AuthService(client=yandex_client)


def get_user_service(user_repository: UserRepository = Depends()) -> UserService:
    return UserService(user_repo=user_repository)
