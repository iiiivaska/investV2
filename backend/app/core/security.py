"""
Утилиты безопасности: хеширование паролей и работа с JWT токенами.
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional, Tuple

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import get_settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
settings = get_settings()


def hash_password(plain_password: str) -> str:
    """Вернуть безопасный хеш пароля."""
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверить соответствие пароля и хеша."""
    return pwd_context.verify(plain_password, hashed_password)


def _create_token(
    subject: str,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: Optional[Dict[str, Any]] = None,
) -> str:
    now = datetime.now(timezone.utc)
    to_encode: Dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": int(now.timestamp()),
        "exp": int((now + expires_delta).timestamp()),
    }
    if extra_claims:
        to_encode.update(extra_claims)
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def create_access_token(user_id: int, email: str) -> str:
    """Создать access-токен для пользователя."""
    expire = timedelta(minutes=settings.access_token_expire_minutes)
    return _create_token(str(user_id), "access", expire, {"email": email})


def create_refresh_token(user_id: int, email: str) -> str:
    """Создать refresh-токен для пользователя."""
    expire = timedelta(days=settings.refresh_token_expire_days)
    return _create_token(str(user_id), "refresh", expire, {"email": email})


def decode_token(token: str) -> Dict[str, Any]:
    """Декодировать и проверить JWT токен. Бросает исключение при ошибке."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as exc:
        raise exc


