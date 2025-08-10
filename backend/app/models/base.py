"""
Базовая модель SQLAlchemy
"""
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Mapped, mapped_column


@as_declarative()
class Base:
    """Базовая модель с общими полями"""

    id: Any
    __name__: str

    # Генерация имени таблицы на основе класса
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    # Общие поля для всех моделей
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
