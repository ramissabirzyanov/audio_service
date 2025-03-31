from pydantic_settings import BaseSettings, SettingsConfigDict


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
    TOKEN_URL: str = "https://oauth.yandex.ru/token"
    USER_INFO_URL: str = "https://login.yandex.ru/info"

    model_config = SettingsConfigDict(
        env_file=".env", extra="allow"
    )



settings = Settings()