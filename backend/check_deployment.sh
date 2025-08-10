#!/bin/bash

# ========================================
# ПРОВЕРКА ГОТОВНОСТИ К РАЗВЕРТЫВАНИЮ INVESTV2
# ========================================

echo "🔍 Проверяем готовность к развертыванию InvestV2..."
echo ""

# Проверяем наличие Docker
echo "🐳 Проверка Docker..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    echo "✅ Docker установлен: $DOCKER_VERSION"
else
    echo "❌ Docker не установлен"
    exit 1
fi

# Проверяем наличие Docker Compose
echo "🐳 Проверка Docker Compose..."
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    echo "✅ Docker Compose установлен: $COMPOSE_VERSION"
else
    echo "❌ Docker Compose не установлен"
    exit 1
fi

# Проверяем подключение к внешней базе данных
echo "🗄️ Проверка подключения к внешней БД..."
if docker run --rm postgres:15-alpine psql "postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2" -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ Подключение к внешней БД успешно"
else
    echo "❌ Не удается подключиться к внешней БД"
    echo "   Проверьте:"
    echo "   - Доступность сервера 192.168.0.4"
    echo "   - Правильность учетных данных"
    echo "   - Открытый порт 5432"
    exit 1
fi

# Проверяем наличие необходимых файлов
echo "📁 Проверка файлов..."
REQUIRED_FILES=("docker-compose.yml" "Dockerfile" "requirements.txt" "env.production")

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file найден"
    else
        echo "❌ $file не найден"
        exit 1
    fi
done

# Проверяем наличие .env файла
echo "⚙️ Проверка конфигурации..."
if [ -f ".env" ]; then
    echo "✅ .env файл найден"
    
    # Проверяем SECRET_KEY
    if grep -q "your-super-secret-production-key-change-this-immediately" .env; then
        echo "⚠️  ВНИМАНИЕ: SECRET_KEY не изменен! Измените его перед развертыванием"
    else
        echo "✅ SECRET_KEY настроен"
    fi
else
    echo "⚠️  .env файл не найден. Создайте его из env.production"
    echo "   cp env.production .env"
fi

# Проверяем права на скрипты
echo "🔧 Проверка скриптов..."
SCRIPTS=("deploy.sh" "dev.sh" "update.sh" "migrate_production.sh")

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        if [ -x "$script" ]; then
            echo "✅ $script исполняемый"
        else
            echo "⚠️  $script найден, но не исполняемый"
            echo "   chmod +x $script"
        fi
    else
        echo "❌ $script не найден"
    fi
done

# Проверяем доступность портов
echo "🔌 Проверка портов..."
if netstat -tuln 2>/dev/null | grep -q ":8000 "; then
    echo "⚠️  Порт 8000 уже занят"
else
    echo "✅ Порт 8000 свободен"
fi

if netstat -tuln 2>/dev/null | grep -q ":6379 "; then
    echo "⚠️  Порт 6379 уже занят"
else
    echo "✅ Порт 6379 свободен"
fi

# Проверяем свободное место
echo "💾 Проверка свободного места..."
FREE_SPACE=$(df -h . | awk 'NR==2 {print $4}')
echo "✅ Свободное место: $FREE_SPACE"

# Проверяем память
echo "🧠 Проверка памяти..."
TOTAL_MEM=$(free -h | awk 'NR==2{print $2}')
FREE_MEM=$(free -h | awk 'NR==2{print $7}')
echo "✅ Общая память: $TOTAL_MEM, Свободная: $FREE_MEM"

echo ""
echo "🎯 Итоговая оценка готовности:"

# Подсчитываем результаты
TOTAL_CHECKS=0
PASSED_CHECKS=0

# Docker и Docker Compose
TOTAL_CHECKS=$((TOTAL_CHECKS + 2))
if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
    PASSED_CHECKS=$((PASSED_CHECKS + 2))
fi

# База данных
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
if docker run --rm postgres:15-alpine psql "postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2" -c "SELECT 1;" > /dev/null 2>&1; then
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
fi

# Файлы
TOTAL_CHECKS=$((TOTAL_CHECKS + 4))
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    fi
done

# Показываем результат
PERCENTAGE=$((PASSED_CHECKS * 100 / TOTAL_CHECKS))

if [ $PERCENTAGE -eq 100 ]; then
    echo "🎉 Готовность: 100% - Система готова к развертыванию!"
    echo ""
    echo "🚀 Для запуска выполните:"
    echo "   ./deploy.sh"
elif [ $PERCENTAGE -ge 80 ]; then
    echo "✅ Готовность: ${PERCENTAGE}% - Почти готово, исправьте предупреждения"
elif [ $PERCENTAGE -ge 60 ]; then
    echo "⚠️  Готовность: ${PERCENTAGE}% - Требует доработки"
else
    echo "❌ Готовность: ${PERCENTAGE}% - Требует серьезной доработки"
fi

echo ""
echo "📊 Результат: $PASSED_CHECKS из $TOTAL_CHECKS проверок пройдено"
