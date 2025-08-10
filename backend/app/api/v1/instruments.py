"""
API endpoints для управления инструментами
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/hello")
async def instruments_hello():
    """Hello World endpoint для инструментов"""
    return {
        "message": "Hello World from Instruments API",
        "module": "instruments",
        "endpoints": [
            "/search",
            "/details",
            "/quotes"
        ]
    }


@router.get("/search")
async def search_instruments():
    """Поиск финансовых инструментов"""
    return {"message": "Instruments search endpoint - coming soon"}


@router.get("/quotes")
async def get_quotes():
    """Получить котировки"""
    return {"message": "Instruments quotes endpoint - coming soon"}
