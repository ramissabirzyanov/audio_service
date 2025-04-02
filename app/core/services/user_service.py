from typing import Optional

from app.core.db.db_repository import UserRepository
from app.core.models.user import User


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_or_create_user(self, user_email):
        "Полученеи или создание нового пользователя в случае его отсутсвия в БД"
        user = await self.user_repo.get_user_by_email(user_email)
        if not user:
            user = await self.user_repo.create_user(user_email)
        return user
    
    async def get_user_by_email(self, user_email):
        "Получение пользователя через его почту"
        return await self.user_repo.get_user_by_email(user_email)
    
    async def get_user_data_by_id(self, user_id: int) -> Optional[User]:
        """Получение данных пользователя"""
        user = await self.user_repo.get_user_data(user_id)
        if not user:
            return {"error": f"User with id {user_id} not found"}
        return user
    
    async def make_superuser(self, user_id: int) -> None:
        """Только для админов: назначение прав суперпользователя"""
        user = await self.user_repo.get_user_by_id(user_id)

        if not user.is_superuser:
            return {"error": f"You don't have rights!"}

        await self.user_repo.make_super_user(user_id)
