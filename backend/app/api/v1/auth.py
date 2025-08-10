"""
API endpoints для авторизации
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def auth_hello():
    """Hello World endpoint для авторизации"""
    return {
        "message": "Hello World from Auth API",
        "module": "authentication",
        "endpoints": [
            "/login",
            "/register", 
            "/refresh",
            "/logout"
        ]
    }


@router.post("/register")
async def register():
    """Регистрация нового пользователя"""
    return {"message": "Register endpoint - coming soon"}


@router.post("/login")
async def login():
    """Вход пользователя"""
    return {"message": "Login endpoint - coming soon"}


@router.post("/refresh")
async def refresh_token():
    """Обновление токена"""
    return {"message": "Refresh token endpoint - coming soon"}


@router.post("/logout")
async def logout():
    """Выход пользователя"""
    return {"message": "Logout endpoint - coming soon"}
