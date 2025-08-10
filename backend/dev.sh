#!/bin/bash

# ========================================
# СКРИПТ ЗАПУСКА INVESTV2 В РЕЖИМЕ РАЗРАБОТКИ
# ========================================

set -e  # Остановка при ошибке

echo "🔧 Запускаем InvestV2 в режиме разработки..."

# Проверяем наличие Docker и Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker сначала."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose сначала."
    exit 1
fi

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose down --remove-orphans

# Собираем и запускаем контейнеры с override для разработки
echo "🔨 Собираем и запускаем контейнеры для разработки..."
docker-compose up --build

echo "🎉 Режим разработки запущен!"
echo "🌐 API доступен по адресу: http://localhost:8000"
echo "📚 Документация: http://localhost:8000/docs"
echo "🗄️ pgAdmin: http://localhost:5050 (admin@investv2.com / admin)"
