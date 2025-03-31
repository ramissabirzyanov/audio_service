from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models.user import User


class DB_Repository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email):
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
