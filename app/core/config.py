from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Collaborative Code Editor"
    API_V1_STR: str = "/api/v1"
    
    # Database
    DATABASE_URL: str
    SQLALCHEMY_DATABASE_URI: str = ""
    REDIS_URL: str
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # OpenAI
    OPENAI_API_KEY: str
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URL
    
    class Config:
        env_file = ".env"
settings = Settings()

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL 