from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from app.core.schemas.user import UserCreate, UserResponse
from app.core.schemas.token import Token
from app.core.services.auth_service import AuthService
from app.api.dependencies import get_current_superuser, get_current_user, get_auth_service
from app.core.db.session import get_db
from app.core.db.db_repository import UserRepository
from app.core.models.user import User


router = APIRouter()


@router.post('/auth/login', response_model=Token)
async def auth_user_with_yandex(
    request: UserCreate,
    db: AsyncSession = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Аутентификация пользователя через Яндекс OAuth.
    Возвращает JWT токен для доступа к API.
    """
    token_data = await auth_service.auth_with_yandex(request.code_from_yandex)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to authenticate with Yandex"
        )

    user = await get_current_user(
        token=token_data.access_token,
        db=db
    )
    await UserRepository.create_user(db, user.email)
    return token_data


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_data(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user = await UserRepository.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found")
    return user