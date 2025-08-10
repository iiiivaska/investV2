"""
Конфигурация приложения
"""
from functools import lru_cache
from typing import Optional

from pydantic import validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    app_name: str = "InvestV2"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # База данных - PostgreSQL по умолчанию
    database_url: str = "postgresql://investv2:password@localhost:5432/investv2"
    
    # PostgreSQL настройки (для локальной разработки)
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "investv2"
    postgres_password: str = "password"
    postgres_db: str = "investv2"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Email
    email_host: Optional[str] = None
    email_port: Optional[int] = None
    email_username: Optional[str] = None
    email_password: Optional[str] = None
    email_from: Optional[str] = None
    
    # Tinkoff API
    tinkoff_token: Optional[str] = None
    tinkoff_sandbox: bool = False
    
    # CORS
    allowed_origins: list = ["*"]
    
    @validator("database_url", pre=True)
    def validate_database_url(cls, v):
        if v and not v.startswith(("postgresql://", "sqlite:///")):
            raise ValueError("Database URL must start with postgresql:// or sqlite:///")
        return v
    
    @property
    def postgresql_url(self) -> str:
        """Создает URL для PostgreSQL из отдельных параметров"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Получить настройки приложения с кешированием"""
    return Settings()
