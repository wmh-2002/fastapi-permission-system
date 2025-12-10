from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "postgresql://username:password@localhost/dbname"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000"]
    
    # Password hashing
    PASSWORD_SALT: str = "your-salt-here"
    
    class Config:
        env_file = ".env"


settings = Settings()