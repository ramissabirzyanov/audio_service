from fastapi import APIRouter, Query
from fastapi import Depends, HTTPException, status

from app.core.schemas.user import UserLogin, UserResponse
from app.core.schemas.token import AuthResponse
from app.core.services.auth_service import AuthService
from app.api.dependencies import get_current_user, get_auth_service, get_user_service
from app.core.services.user_service import UserService
from app.core.models.user import User


router = APIRouter()


@router.post("/auth/login", response_model=AuthResponse)
async def auth_user_with_yandex(
    code: str = Query(..., alias="code"),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Аутентификация пользователя через Яндекс OAuth.
    Возвращает JWT токен для доступа к API.
    """
    auth_data = await auth_service.auth_with_yandex(code)
    if not auth_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to authenticate with Yandex"
        )
    return auth_data


@router.get('/users/{user_id}', response_model=UserResponse)
async def get_user_data(
    user_id: int,
    current_user: UserResponse = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
):
    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have rigths!"
        )
    return current_user
    # user = await user_service.get_user_data_by_id(user_id)
    # return UserResponse.model_validate(user)
