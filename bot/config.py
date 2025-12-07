from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    MIN_TEXT_LENGTH: int

    class Config:
        env_file=".env"

settings=Settings()