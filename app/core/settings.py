from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Класс для хранения настроек приложения, загружаемых из переменных окружения.
    """
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str
    TOKEN_URL = "https://oauth.yandex.ru/token"
    INFO_URL = "https://login.yandex.ru/info"

    class Config:
        env_file = ".env"

settings = Settings()