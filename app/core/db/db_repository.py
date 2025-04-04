from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from sqlalchemy.orm import selectinload

from app.core.models.user import User
from app.core.models.audio_file import AudioFile


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_user_data(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.audio_files))
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, email: str) -> User:
        new_user = User(email=email)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def update_user(self, user_id: int, user_data: dict) -> None:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(
                email=user_data['email'],
                is_superuser=user_data['is_superuser']
            )
        )
        await self.db.commit()

    async def get_user_by_id(self, user_id: int) -> User:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def make_super_user(self, user_id: int) -> None:
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_superuser=True)
        )
        await self.db.commit()

    async def delete_user(self, user_id: int) -> None:
        await self.db.execute(
            delete(User)
            .where(User.id == user_id)
        )
        await self.db.commit()


class AudioRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_audio_file(
        self,
        user_id: int,
        filename: str,
        file_path: str
    ) -> AudioFile:
        """
        Добавление аудио файла.
        """
        audio = AudioFile(
            user_id=user_id,
            filename=filename,
            path=file_path
        )
        self.db.add(audio)
        await self.db.commit()
        await self.db.refresh(audio)
        return audio
    
    async def update_audio_file(self, audi_data, audio_id):
        await self.db.execute(
            update(AudioFile)
            .where(AudioFile.id == audio_id)
            .values(
                filename=audi_data['filename'],
                path=audi_data['path']
            )
        )
        await self.db.commit()

    async def delete_audio_file(self, audio_id: int) -> None:
        await self.db.execute(
            delete(AudioFile)
            .where(AudioFile.id == audio_id)
        )
        await self.db.commit()

    async def get_user_audio_files(
        self, 
        user_id: int,
        limit: int = 50,
        offset: int = 0
    ) -> list[AudioFile]:
        """Получает все аудиофайлы пользователя с пагинацией"""
        result = await self.db.execute(
            select(AudioFile)
            .where(AudioFile.user_id == user_id)
            .order_by(AudioFile.filename)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
