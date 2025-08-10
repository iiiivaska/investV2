"""
API endpoints для управления пользователями
"""
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserRead

router = APIRouter()


@router.get("/hello")
async def users_hello():
    """Hello World endpoint для пользователей"""
    return {
        "message": "Hello World from Users API",
        "module": "users",
        "endpoints": ["/me", "/profile", "/settings"],
    }


@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    """Получить информацию о текущем пользователе"""
    return UserRead.model_validate(current_user)


@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)) -> dict:
    """Получить профиль пользователя"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
    }


class TinkoffTokenUpdate(BaseModel):
    tinkoff_api_token: str


@router.post("/tinkoff-token", status_code=status.HTTP_204_NO_CONTENT)
def set_tinkoff_token(
    payload: TinkoffTokenUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> None:
    """Установить/обновить Tinkoff API токен для текущего пользователя."""
    if not payload.tinkoff_api_token:
        raise HTTPException(status_code=400, detail="Token is required")
    current_user.tinkoff_api_token = payload.tinkoff_api_token
    db.add(current_user)
    db.commit()
