from functools import lru_cache

from pydantic_settings import BaseSettings

1
class AppSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEVELOPMENT_MODE: bool = False
    MODEL_PATH: str = "artifacts/models"


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
