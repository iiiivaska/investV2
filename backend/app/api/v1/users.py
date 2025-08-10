"""
API endpoints для управления пользователями
"""
from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
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
