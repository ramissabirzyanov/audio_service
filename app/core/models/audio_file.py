from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer

from app.core.db.base import Base

if TYPE_CHECKING:
    from app.core.models.user import User


class AudioFile(Base):
    __tablename__ = "audio_files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    filename: Mapped[str] = mapped_column(String)
    path: Mapped[str] = mapped_column(String)
    user: Mapped["User"] = relationship(back_populates="audio_files")
