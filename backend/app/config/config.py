from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()
print("db url", os.environ.get("DATABASE_URL"))


class Settings(BaseSettings):
    # Application Settings
    PROJECT_NAME: str = os.environ.get("PROJECT_NAME")
    API_V1_STR: str = os.environ.get("API_V1_STR")
    DATABASE_URL: str = os.environ.get("DATABASE_URL")
    ALLOWED_ORIGINS: str = os.environ.get("ALLOWED_ORIGINS")
    # Authentication
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
