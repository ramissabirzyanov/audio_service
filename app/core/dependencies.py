from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.settings import settings
from app.core.services.db_repository import DB_Repository
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_db
from app.core.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/yandex")

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    db_repo = DB_Repository(db)
    user = await db_repo.get_user_by_email(email)
    if user is None:
        raise credentials_exception
    return user

async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Permission denied")
    return current_user
