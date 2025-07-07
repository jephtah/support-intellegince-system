from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):

    DATABASE_URL: str = os.getenv("DATABASE_URL")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    API_PREFIX: str = os.getenv("API_PREFIX", "/api")
    
    # TODO: add redis config for caching
    # TODO: add sentry config for monitoring

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()