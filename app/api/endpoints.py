from fastapi import APIRouter
from fastapi import Depends, HTTPException, status

from app.core.schemas.user import UserLogin, UserResponse
from app.core.schemas.token import AuthResponse
from app.core.services.auth_service import AuthService
from app.api.dependencies import get_current_user, get_auth_service
from app.core.services.user_service import UserService
from app.core.models.user import User


router = APIRouter()


@router.post('/auth/login', response_model=AuthResponse)
async def auth_user_with_yandex(
    request: UserLogin,
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
    return token_data


@router.get('/{user_id}', response_model=UserResponse)
async def get_user_data(
    user_id: int,
    current_user: User = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have rigths!"
        )
    return UserResponse.model_validate(current_user)
