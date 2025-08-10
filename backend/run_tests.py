#!/usr/bin/env python3
"""
Скрипт для запуска тестов локально
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(command: str, description: str) -> bool:
    """Запускает команду и возвращает True если успешно"""
    print(f"\n🔧 {description}")
    print(f"Команда: {command}")
    print("-" * 50)
    
    result = subprocess.run(command, shell=True, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print(f"✅ {description} - УСПЕШНО")
        return True
    else:
        print(f"❌ {description} - ОШИБКА")
        return False

def main():
    """Основная функция"""
    print("🚀 Запуск тестов для InvestV2")
    print("=" * 50)
    
    # Проверяем, что мы в правильной директории
    if not Path("requirements.txt").exists():
        print("❌ Файл requirements.txt не найден. Убедитесь, что вы в директории backend/")
        sys.exit(1)
    
    # Устанавливаем переменные окружения для тестов
    os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
    os.environ.setdefault("SECRET_KEY", "test-secret-key-for-local-tests")
    os.environ.setdefault("ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    os.environ.setdefault("REFRESH_TOKEN_EXPIRE_DAYS", "7")
    os.environ.setdefault("TINKOFF_API_TOKEN", "test-token")
    
    success = True
    
    # Линтинг
    success &= run_command("flake8 app tests", "Проверка стиля кода (flake8)")
    success &= run_command("black --check app tests", "Проверка форматирования (black)")
    success &= run_command("isort --check-only app tests", "Проверка импортов (isort)")
    
    # Тесты
    success &= run_command("pytest tests/ -v --tb=short", "Запуск тестов (pytest)")
    
    # Покрытие кода
    success &= run_command(
        "pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html",
        "Проверка покрытия кода"
    )
    
    # Безопасность
    success &= run_command("bandit -r app", "Проверка безопасности (bandit)")
    success &= run_command("safety scan", "Проверка уязвимостей зависимостей (safety)")
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ УСПЕШНО!")
        print("✅ Код готов к коммиту")
        sys.exit(0)
    else:
        print("❌ НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОШЛИ")
        print("🔧 Исправьте ошибки перед коммитом")
        sys.exit(1)

if __name__ == "__main__":
    main()
