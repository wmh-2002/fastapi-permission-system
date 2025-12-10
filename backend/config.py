from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # 数据库设置
    DATABASE_URL: str = "postgresql://username:password@localhost/dbname"
    
    # JWT 设置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS 设置
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000"]
    
    # 密码哈希
    PASSWORD_SALT: str = "your-salt-here"
    
    class Config:
        env_file = ".env"


settings = Settings()