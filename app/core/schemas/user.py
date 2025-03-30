from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    created_at: datetime


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
