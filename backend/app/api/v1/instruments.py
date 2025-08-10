"""
API endpoints для управления инструментами
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database.database import get_db
from app.models.user import User
from app.TInvest_Engine.client import TInvestClient

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
            "/quotes",
            "/tinkoff-demo",
        ],
    }


@router.get("/search")
async def search_instruments():
    """Поиск финансовых инструментов"""
    return {"message": "Instruments search endpoint - coming soon"}


@router.get("/quotes")
async def get_quotes():
    """Получить котировки"""
    return {"message": "Instruments quotes endpoint - coming soon"}


@router.get("/tinkoff-demo")
def tinkoff_demo(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Демонстрационный вызов к Tinkoff Invest API с использованием токена пользователя.

    Берет токен из поля `tinkoff_api_token` пользователя, вызывает продовый API и возвращает ответ.
    В качестве демонстрации запрашиваем список аккаунтов пользователя.
    """
    if not current_user.tinkoff_api_token:
        raise HTTPException(
            status_code=400, detail="Tinkoff API token is not set for this user"
        )

    try:
        with TInvestClient(current_user.tinkoff_api_token) as ti:
            accounts = [account.__dict__ for account in ti.list_accounts()]
        return {
            "source": "tinkoff",
            "endpoint": "users.get_accounts",
            "accounts": accounts,
        }
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=502, detail=f"Tinkoff API call failed: {exc}")
