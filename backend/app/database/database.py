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
    
    # Проверяем, есть ли конфигурация БД
    if not settings.has_database_config:
        print("Database configuration not found, skipping database initialization")
        return False
    
    try:
        database_url = settings.postgresql_url
        if not database_url:
            print("Database URL is empty, skipping database initialization")
            return False
            
        pool_kwargs = {
            "poolclass": QueuePool,
            "pool_size": 10,
            "max_overflow": 20,
            "pool_pre_ping": True,
            "pool_recycle": 3600,  # Пересоздаем соединения каждый час
            "echo": False,
        }
        
        engine = create_engine(database_url, **pool_kwargs)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Тестируем подключение
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        print("Database connection established successfully")
        return True
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        print("Application will continue without database")
        engine = None
        SessionLocal = None
        return False

def get_db() -> Generator:
    """Получить сессию базы данных"""
    if SessionLocal is None:
        print("Database not available")
        yield None
        return
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
