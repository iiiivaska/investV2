"""
Настройка подключения к базе данных PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from typing import Generator

from app.core.config import get_settings

settings = get_settings()

# Используем PostgreSQL URL
database_url = settings.postgresql_url

# Параметры пула соединений для PostgreSQL
pool_kwargs = {
    "poolclass": QueuePool,
    "pool_size": 10,
    "max_overflow": 20,
    "pool_pre_ping": True,
    "pool_recycle": 3600,  # Пересоздаем соединения каждый час
    "echo": settings.debug
}

# Создание движка базы данных
engine = create_engine(
    database_url,
    **pool_kwargs
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
