#!/usr/bin/env python3
"""
Скрипт для быстрого запуска приложения в режиме разработки
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["app"],
        log_level="info"
    )
