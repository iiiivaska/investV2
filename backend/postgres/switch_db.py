#!/usr/bin/env python3
"""
Скрипт для проверки статуса PostgreSQL базы данных
"""
import os
import sys
import shutil
from pathlib import Path

def show_current_db():
    """Показать текущую базу данных"""
    print("📊 Текущая база данных: PostgreSQL")
    print("📋 Настройки:")
    
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "postgresql" in content.lower():
                print("✅ Конфигурация PostgreSQL найдена в .env")
            else:
                print("⚠️  Конфигурация PostgreSQL не найдена в .env")
    else:
        print("⚠️  Файл .env не найден")

def check_postgresql_connection():
    """Проверка подключения к PostgreSQL"""
    try:
        import psycopg2
        from app.core.config import get_settings
        
        settings = get_settings()
        
        # Тестируем подключение
        conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db
        )
        conn.close()
        print("✅ Подключение к PostgreSQL успешно!")
        return True
        
    except ImportError:
        print("❌ psycopg2 не установлен")
        print("💡 Установите: pip install psycopg2-binary")
        return False
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        print("\n🔧 Убедитесь, что:")
        print("1. PostgreSQL сервер запущен")
        print("2. Пользователь и БД созданы")
        print("3. Параметры подключения корректны")
        return False

def main():
    """Основная функция"""
    print("🚀 InvestV2 - Статус PostgreSQL")
    print("=" * 40)
    
    if len(sys.argv) < 2:
        show_current_db()
        print("\n📋 Дополнительные команды:")
        print("  python3 postgres/switch_db.py status    - показать текущий статус")
        print("  python3 postgres/switch_db.py check     - проверить подключение")
        return
    
    command = sys.argv[1].lower()
    
    if command == "status":
        show_current_db()
    elif command == "check":
        check_postgresql_connection()
    else:
        print(f"❌ Неизвестная команда: {command}")
        print("\n📋 Доступные команды:")
        print("  status   - показать текущий статус")
        print("  check    - проверить подключение")

if __name__ == "__main__":
    main()
