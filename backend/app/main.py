"""
Главный модуль FastAPI приложения InvestV2
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import analytics, auth, instruments, portfolio, users
from app.core.config import get_settings
from app.database.database import init_database

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

# API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(portfolio.router, prefix="/api/v1/portfolio", tags=["portfolio"])
app.include_router(
    instruments.router, prefix="/api/v1/instruments", tags=["instruments"]
)
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])


@app.on_event("startup")
async def startup_event():
    """Инициализация при старте"""
    print("Starting InvestV2 API...")
    print("Initializing database connection...")
    try:
        init_database()
        print("Database initialization completed")
    except Exception as e:
        print(f"Database initialization failed: {e}")
        print("Application will continue without database")
    print("InvestV2 API startup completed")


@app.get("/")
async def root():
    """Базовый endpoint для проверки работоспособности API"""
    return {
        "message": "Hello World from InvestV2 API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/test")
async def test():
    """Простой тестовый endpoint без зависимостей"""
    return {
        "message": "Test endpoint working!",
        "timestamp": "2024-01-01T00:00:00Z",
        "status": "ok"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "InvestV2 API is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
