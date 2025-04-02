from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.settings import settings
from app.core.db.db_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.models.user import User
from app.core.services.yandex_api_service import YandexApiService
from app.core.services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return "Could not validate data"

    email = payload.get("sub")
    
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied"
        )
    return current_user


def get_auth_service(yandex_service: YandexApiService = Depends()) -> AuthService:
    return AuthService(client=yandex_service)
