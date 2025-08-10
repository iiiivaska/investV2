"""
Настройка подключения к базе данных
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Generator

from app.core.config import get_settings

settings = get_settings()

# Создание движка базы данных
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.debug  # Логирование SQL запросов в debug режиме
)

# Фабрика сессий
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Generator:
    """Dependency для получения сессии БД"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
