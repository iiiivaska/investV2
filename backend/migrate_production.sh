#!/bin/bash

# ========================================
# СКРИПТ ПРИМЕНЕНИЯ МИГРАЦИЙ В ПРОДАКШН БД
# ========================================

set -e  # Остановка при ошибке

echo "🗄️ Применяем миграции в продакшн базе данных..."

# Проверяем подключение к внешней базе данных
echo "🔍 Проверяем подключение к внешней базе данных..."

# Устанавливаем переменные окружения для продакшн БД
export DATABASE_URL="postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2"

# Проверяем подключение
if ! python3 -c "
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

try:
    engine = create_engine(os.getenv('DATABASE_URL'))
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✅ Подключение к БД успешно')
except SQLAlchemyError as e:
    print(f'❌ Ошибка подключения к БД: {e}')
    exit(1)
" 2>/dev/null; then
    echo "❌ Не удается подключиться к внешней базе данных"
    exit 1
fi

echo "✅ Подключение к базе данных успешно"

# Проверяем текущий статус миграций
echo "📊 Текущий статус миграций:"
python3 migrate.py status

# Применяем миграции
echo "🔄 Применяем миграции..."
python3 migrate.py upgrade

echo "✅ Миграции успешно применены!"

# Проверяем финальный статус
echo "📊 Финальный статус миграций:"
python3 migrate.py status

echo "🎉 Миграции завершены!"
