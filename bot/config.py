from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    MIN_TEXT_LENGTH: int
    
    ML_MODEL_PATH: str = "models/complete_model.keras"
    TOKENIZER_PATH: str = "tokenizers/tokenizer.pkl"
    
    VIRAL_THRESHOLD: float = 0.5
    MIN_TEXT_LENGTH: int = 10
    MAX_TEXT_LENGTH: int = 5000
    
    ENABLE_EMOJIS: bool = True
    class Config:
        env_file=".env"

settings=Settings()