#!/usr/bin/env python3
"""
Скрипт для инициализации PostgreSQL базы данных
"""
import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from app.core.config import get_settings

def init_postgres():
    """Инициализация PostgreSQL базы данных"""
    settings = get_settings()
    
    print("🔧 Инициализация PostgreSQL базы данных...")
    
    try:
        # Подключаемся к PostgreSQL серверу (не к конкретной БД)
        conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database="postgres"  # Подключаемся к системной БД
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Проверяем, существует ли база данных
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.postgres_db,))
        exists = cursor.fetchone()
        
        if not exists:
            print(f"📦 Создаем базу данных '{settings.postgres_db}'...")
            cursor.execute(f"CREATE DATABASE {settings.postgres_db}")
            print(f"✅ База данных '{settings.postgres_db}' создана успешно!")
        else:
            print(f"✅ База данных '{settings.postgres_db}' уже существует")
        
        cursor.close()
        conn.close()
        
        # Тестируем подключение к созданной БД
        test_conn = psycopg2.connect(
            host=settings.postgres_host,
            port=settings.postgres_port,
            user=settings.postgres_user,
            password=settings.postgres_password,
            database=settings.postgres_db
        )
        test_conn.close()
        print("✅ Подключение к базе данных успешно!")
        
    except psycopg2.OperationalError as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        print("\n🔧 Убедитесь, что:")
        print("1. PostgreSQL сервер запущен")
        print("2. Параметры подключения корректны")
        print("3. Пользователь имеет права на создание БД")
        return False
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {e}")
        return False
    
    return True

def main():
    """Основная функция"""
    print("🚀 InvestV2 - Инициализация PostgreSQL")
    print("=" * 50)
    
    if init_postgres():
        print("\n🎉 Инициализация завершена успешно!")
        print("\n📋 Следующие шаги:")
        print("1. Запустите миграции: python migrate.py upgrade")
        print("2. Запустите приложение: python run_dev.py")
    else:
        print("\n❌ Инициализация не удалась")
        sys.exit(1)

if __name__ == "__main__":
    main()
