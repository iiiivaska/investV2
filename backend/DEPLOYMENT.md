# 🚀 Развертывание InvestV2 на сервере

## 📋 Требования к серверу

- **Docker** (версия 20.10+)
- **Docker Compose** (версия 2.0+)
- **Доступ к внешней PostgreSQL базе данных**
- **Минимум 2GB RAM**
- **10GB свободного места**

## 🔧 Подготовка к развертыванию

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-username/investV2.git
cd investV2/backend
```

### 2. Настройка переменных окружения

Скопируйте файл с продакшн настройками:

```bash
cp env.production .env
```

**ВАЖНО**: Отредактируйте `.env` файл и обязательно измените:

- `SECRET_KEY` - сгенерируйте новый секретный ключ
- `ALLOWED_ORIGINS` - укажите ваш домен
- `EMAIL_*` - настройте email для уведомлений

### 3. Генерация секретного ключа

```bash
# Генерируем секретный ключ
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Скопируйте результат в `SECRET_KEY` в файле `.env`.

## 🚀 Развертывание

### Автоматическое развертывание

```bash
# Делаем скрипт исполняемым
chmod +x deploy.sh

# Запускаем развертывание
./deploy.sh
```

### Ручное развертывание

```bash
# Останавливаем существующие контейнеры
docker-compose down --remove-orphans

# Собираем и запускаем
docker-compose up --build -d

# Проверяем статус
docker-compose ps

# Смотрим логи
docker-compose logs -f api
```

## 🔍 Проверка развертывания

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Ожидаемый ответ:
```json
{"status": "healthy", "timestamp": "2024-01-01T12:00:00Z"}
```

### 2. Основной endpoint

```bash
curl http://localhost:8000/
```

### 3. Документация API

Откройте в браузере: `http://localhost:8000/docs`

## 🗄️ Настройка базы данных

### Создание базы данных

Подключитесь к вашей PostgreSQL серверу и создайте базу данных:

```sql
CREATE DATABASE investv2;
```

### Применение миграций

```bash
# Входим в контейнер
docker-compose exec api bash

# Применяем миграции
python migrate.py upgrade
```

## 🔧 Управление приложением

### Просмотр логов

```bash
# Все сервисы
docker-compose logs -f

# Только API
docker-compose logs -f api

# Только Redis
docker-compose logs -f redis
```

### Остановка приложения

```bash
docker-compose down
```

### Перезапуск

```bash
docker-compose restart api
```

### Обновление

```bash
# Останавливаем
docker-compose down

# Обновляем код
git pull

# Пересобираем и запускаем
docker-compose up --build -d
```

## 🛡️ Безопасность

### 1. Firewall

Настройте firewall для открытия только необходимых портов:

```bash
# Открываем только порт 8000 для API
sudo ufw allow 8000/tcp

# Открываем SSH (если нужно)
sudo ufw allow ssh
```

### 2. Reverse Proxy (рекомендуется)

Настройте Nginx как reverse proxy:

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. SSL/HTTPS

Настройте SSL сертификат (Let's Encrypt):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com
```

## 📊 Мониторинг

### 1. Статус контейнеров

```bash
docker-compose ps
```

### 2. Использование ресурсов

```bash
docker stats
```

### 3. Логи приложения

```bash
docker-compose logs --tail=100 api
```

## 🔄 Обновление приложения

### Автоматическое обновление

```bash
# Создайте скрипт update.sh
chmod +x update.sh
./update.sh
```

### Ручное обновление

```bash
# Останавливаем
docker-compose down

# Обновляем код
git pull origin main

# Пересобираем
docker-compose up --build -d

# Проверяем
curl http://localhost:8000/health
```

## 🆘 Устранение неполадок

### Приложение не запускается

1. Проверьте логи:
```bash
docker-compose logs api
```

2. Проверьте подключение к БД:
```bash
docker-compose exec api python -c "
from app.database.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT 1'))
    print('DB connection OK')
"
```

3. Проверьте переменные окружения:
```bash
docker-compose exec api env | grep -E "(DATABASE|SECRET)"
```

### Проблемы с базой данных

1. Проверьте подключение:
```bash
docker run --rm postgres:15-alpine psql "postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2" -c "SELECT 1;"
```

2. Проверьте права доступа пользователя БД

### Проблемы с Redis

```bash
docker-compose exec redis redis-cli ping
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `docker-compose logs -f`
2. Проверьте статус контейнеров: `docker-compose ps`
3. Проверьте health check: `curl http://localhost:8000/health`
4. Создайте issue в GitHub с логами и описанием проблемы
