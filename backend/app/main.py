"""
Главный модуль FastAPI приложения InvestV2
"""
import os
import subprocess
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import analytics, auth, instruments, portfolio, users
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="InvestV2 API",
    description="API для управления инвестиционным портфелем с интеграцией Tinkoff Invest",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Автоматический запуск миграций при старте приложения (опционально)
@app.on_event("startup")
async def run_migrations_on_startup() -> None:
    if not settings.run_migrations_on_startup:
        return
    # Учитываем DATABASE_URL из окружения, alembic его подхватит из env.py
    try:
        subprocess.run(
            ["python", os.path.join(os.path.dirname(__file__), "..", "migrate.py"), "upgrade"],
            check=True,
        )
    except Exception:
        # Не прерываем запуск приложения, если миграции не удались
        # Логи uvicorn покажут ошибку выполнения
        pass

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["portfolio"])
app.include_router(
    instruments.router, prefix="/api/v1/instruments", tags=["instruments"]
)
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.get("/")
async def root():
    """Базовый endpoint для проверки работоспособности API"""
    return {
        "message": "Hello World from InvestV2 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "InvestV2 API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
