"""
API endpoints для управления портфелем
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def portfolio_hello():
    """Hello World endpoint для портфеля"""
    return {
        "message": "Hello World from Portfolio API",
        "module": "portfolio",
        "endpoints": ["/positions", "/performance", "/history"],
    }


@router.get("/positions")
async def get_positions():
    """Получить позиции портфеля"""
    return {"message": "Portfolio positions endpoint - coming soon"}


@router.get("/performance")
async def get_performance():
    """Получить доходность портфеля"""
    return {"message": "Portfolio performance endpoint - coming soon"}
