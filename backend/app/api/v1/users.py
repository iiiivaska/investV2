"""
API endpoints для управления пользователями
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def users_hello():
    """Hello World endpoint для пользователей"""
    return {
        "message": "Hello World from Users API",
        "module": "users",
        "endpoints": [
            "/me",
            "/profile",
            "/settings"
        ]
    }


@router.get("/me")
async def get_current_user():
    """Получить информацию о текущем пользователе"""
    return {"message": "Current user endpoint - coming soon"}


@router.get("/profile")
async def get_user_profile():
    """Получить профиль пользователя"""
    return {"message": "User profile endpoint - coming soon"}
