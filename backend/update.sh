#!/bin/bash

# ========================================
# СКРИПТ ОБНОВЛЕНИЯ INVESTV2 НА СЕРВЕРЕ
# ========================================

set -e  # Остановка при ошибке

echo "🔄 Начинаем обновление InvestV2..."

# Проверяем наличие Docker и Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен."
    exit 1
fi

# Сохраняем текущие настройки
echo "💾 Сохраняем текущие настройки..."
if [ -f .env ]; then
    cp .env .env.backup
    echo "✅ Настройки сохранены в .env.backup"
fi

# Обновляем код из Git
echo "📥 Обновляем код из Git..."
if ! git pull origin main; then
    echo "❌ Ошибка при обновлении кода из Git"
    exit 1
fi

# Восстанавливаем настройки если нужно
if [ -f .env.backup ] && [ ! -f .env ]; then
    echo "🔄 Восстанавливаем настройки..."
    cp .env.backup .env
fi

# Останавливаем контейнеры
echo "🛑 Останавливаем контейнеры..."
docker-compose down

# Удаляем старые образы
echo "🧹 Очищаем старые образы..."
docker system prune -f

# Пересобираем и запускаем
echo "🔨 Пересобираем и запускаем..."
docker-compose up --build -d

# Ждем запуска
echo "⏳ Ждем запуска приложения..."
sleep 15

# Проверяем статус
echo "📊 Статус контейнеров:"
docker-compose ps

# Проверяем health check
echo "🏥 Проверяем health check..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Обновление завершено успешно!"
    echo "🌐 API доступен по адресу: http://localhost:8000"
    echo "📚 Документация: http://localhost:8000/docs"
else
    echo "❌ Приложение не отвечает после обновления"
    echo "📋 Логи приложения:"
    docker-compose logs api
    echo "🔄 Откатываемся к предыдущей версии..."
    git reset --hard HEAD~1
    docker-compose up --build -d
    exit 1
fi

echo "🎉 Обновление завершено!"
