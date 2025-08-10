#!/bin/bash

# ========================================
# СКРИПТ РАЗВЕРТЫВАНИЯ INVESTV2 НА СЕРВЕРЕ
# ========================================

set -e  # Остановка при ошибке

echo "🚀 Начинаем развертывание InvestV2 на сервере..."

# Проверяем наличие Docker и Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker сначала."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Установите Docker Compose сначала."
    exit 1
fi

# Проверяем подключение к внешней базе данных
echo "🔍 Проверяем подключение к внешней базе данных..."
if ! docker run --rm postgres:15-alpine psql "postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "❌ Не удается подключиться к внешней базе данных. Проверьте настройки."
    exit 1
fi
echo "✅ Подключение к базе данных успешно"

# Останавливаем существующие контейнеры
echo "🛑 Останавливаем существующие контейнеры..."
docker-compose down --remove-orphans

# Удаляем старые образы (опционально)
echo "🧹 Очищаем старые образы..."
docker system prune -f

# Собираем и запускаем контейнеры
echo "🔨 Собираем и запускаем контейнеры..."
docker-compose up --build -d

# Ждем запуска приложения
echo "⏳ Ждем запуска приложения..."
sleep 10

# Проверяем статус контейнеров
echo "📊 Статус контейнеров:"
docker-compose ps

# Проверяем health check
echo "🏥 Проверяем health check..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Приложение успешно запущено!"
    echo "🌐 API доступен по адресу: http://localhost:8000"
    echo "📚 Документация: http://localhost:8000/docs"
else
    echo "❌ Приложение не отвечает на health check"
    echo "📋 Логи приложения:"
    docker-compose logs api
    exit 1
fi

echo "🎉 Развертывание завершено успешно!"
