from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import selectinload

from app.core.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_user_with_audio(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.audio_files))
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, email: str) -> User:
        new_user =  User(email=email)
        await self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                email=user_data['email'],
                is_superuser=user_data['is_superuser']
            )
        )
        await self.db.commit()

