"""
Настройка подключения к базе данных PostgreSQL
"""
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from app.core.config import get_settings

settings = get_settings()

# Инициализация engine как None
engine: Optional[object] = None
SessionLocal: Optional[object] = None

def init_database():
    """Инициализация подключения к БД"""
    global engine, SessionLocal
    
    try:
        database_url = settings.postgresql_url
        pool_kwargs = {
            "poolclass": QueuePool,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # Пересоздаем соединения каждый час
            "echo": settings.debug,
        }
        
        engine = create_engine(database_url, **pool_kwargs)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("Database connection established successfully")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        print("Application will run without database functionality")
        return False

def get_db() -> Generator:
    """Dependency для получения сессии БД"""
    if SessionLocal is None:
        # Возвращаем None если БД недоступна
        yield None
        return
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
