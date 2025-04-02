from pydantic import BaseModel, ConfigDict


class AudioFileBase(BaseModel):
    filename: str


class AudioRequest(AudioFileBase):
    audio_body_base64: str


class AudioFileResponse(AudioFileBase):
    id: int
    path: str

    model_config = ConfigDict(
        from_attributes=True
    )
