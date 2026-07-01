from pydantic_settings import BaseSettings
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    RATE_LIMIT_ENABLED: bool = True

    ENV: str = "development"
    PORT: int = 8000
    USE_HTTPS: bool = False
    SSL_KEYFILE: str | None = None
    SSL_CERTFILE: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()