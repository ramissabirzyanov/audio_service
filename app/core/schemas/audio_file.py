from pydantic import BaseModel, ConfigDict


class AudioFileBase(BaseModel):
    filename: str
    path: str

class AudioFileResponse(AudioFileBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
