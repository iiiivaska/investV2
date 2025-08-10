"""
Pydantic схемы для авторизации
"""
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Схема токена доступа"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Данные токена"""
    user_id: Optional[int] = None
    email: Optional[str] = None


class LoginRequest(BaseModel):
    """Запрос на вход"""
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    """Запрос на обновление токена"""
    refresh_token: str
