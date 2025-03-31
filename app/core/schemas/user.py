from datetime import datetime, timezone
from pydantic import BaseModel, EmailStr, ConfigDict

from app.core.schemas.audio_file import AudioFileBase


class UserBase(BaseModel):
    email: EmailStr
    is_superuser: bool = False
    audio_files: list[AudioFileBase] = []

class UserResponse(UserBase):
    id: int
    created_at: datetime = datetime.now(timezone.utc)

    model_config = ConfigDict(
        from_attributes=True
    )

class UserCreate(UserBase):
    code_from_yandex: str


class UserUpdate(UserBase):
    pass


