import base64
import os
import aiofiles
from fastapi import Depends

from app.core.db.db_repository import AudioRepository
from app.core.db.session import get_db

class AudioServive:
    def __init__(self, audio_repo: AudioRepository = Depends(get_db)):
        self.audio_repo = audio_repo

    @staticmethod
    async def save_audio_file(audio_file_base64: str, filename: str):
        upload_dir = "uploads/audio"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.abspath(os.path.join(upload_dir, filename))
        try:
            audio_bytes = base64.b64decode(audio_file_base64)
        except ValueError as e:
            return {
                "error": "Value error",
                "message": f"Check your base64 data: {str(e)}"
            }

        try:
            async with aiofiles.open(file_path, "wb") as f:
                await f.write(audio_bytes)
        except PermissionError as e:
            return {
                "error": "PermissionError",
                "message": f"You don't have rights!: {str(e)}"
            }

        return file_path

