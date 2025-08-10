# 📋 Обзор файлов развертывания InvestV2

## 🎯 Цель

Настроить развертывание InvestV2 на сервере с использованием внешней PostgreSQL базы данных (192.168.0.4) через Docker Compose.

## 📁 Созданные файлы

### 🔧 Основные конфигурации

| Файл | Описание |
|------|----------|
| `docker-compose.yml` | Основная конфигурация для продакшна (без PostgreSQL) |
| `docker-compose.override.yml` | Переопределения для разработки (с локальной PostgreSQL) |
| `env.production` | Переменные окружения для продакшна |
| `nginx.conf.example` | Пример конфигурации Nginx для reverse proxy |

### 🚀 Скрипты развертывания

| Скрипт | Описание |
|--------|----------|
| `deploy.sh` | Полное развертывание на сервере |
| `dev.sh` | Запуск в режиме разработки |
| `update.sh` | Обновление приложения |
| `migrate_production.sh` | Применение миграций к внешней БД |
| `check_deployment.sh` | Проверка готовности к развертыванию |

### 📚 Документация

| Файл | Описание |
|------|----------|
| `DEPLOYMENT.md` | Подробное руководство по развертыванию |
| `QUICK_DEPLOY.md` | Быстрое развертывание (5 минут) |
| `ssl_setup.md` | Настройка SSL/HTTPS |

## 🔄 Логика работы

### Разработка
```bash
./dev.sh
```
- Запускает FastAPI + PostgreSQL + Redis + pgAdmin
- Использует локальную базу данных
- Включает отладочный режим

### Продакшн
```bash
./deploy.sh
```
- Запускает только FastAPI + Redis
- Подключается к внешней БД (192.168.0.4)
- Продакшн настройки безопасности

## 🗄️ База данных

### Параметры внешней БД
- **Хост**: 192.168.0.4
- **Пользователь**: gen_user
- **Пароль**: %1umkt{~ZFy#m4
- **База данных**: investv2

### Миграции
```bash
# Применение миграций к внешней БД
./migrate_production.sh

# Проверка статуса
python3 migrate.py status
```

## 🔐 Безопасность

### Обязательные изменения перед развертыванием
1. **SECRET_KEY** - сгенерировать новый ключ
2. **ALLOWED_ORIGINS** - указать ваш домен
3. **EMAIL_* настройки** - настроить email

### Генерация секретного ключа
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🚀 Быстрый старт

### 1. Проверка готовности
```bash
./check_deployment.sh
```

### 2. Настройка
```bash
cp env.production .env
# Отредактировать .env файл
```

### 3. Развертывание
```bash
./migrate_production.sh
./deploy.sh
```

### 4. Проверка
```bash
curl http://localhost:8000/health
```

## 📊 Мониторинг

### Логи
```bash
# Все сервисы
docker-compose logs -f

# Только API
docker-compose logs -f api
```

### Статус
```bash
docker-compose ps
docker stats
```

## 🔄 Обновление

### Автоматическое
```bash
./update.sh
```

### Ручное
```bash
git pull
docker-compose down
docker-compose up --build -d
```

## 🆘 Устранение неполадок

### Проверка подключения к БД
```bash
docker run --rm postgres:15-alpine psql "postgresql://gen_user:%1umkt{~ZFy#m4@192.168.0.4:5432/investv2" -c "SELECT 1;"
```

### Проверка приложения
```bash
curl http://localhost:8000/health
docker-compose logs api
```

## 📞 Поддержка

- **Проблемы с развертыванием**: [DEPLOYMENT.md](DEPLOYMENT.md)
- **Быстрый старт**: [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
- **SSL настройка**: [ssl_setup.md](ssl_setup.md)
- **Миграции БД**: [migrations/README.md](migrations/README.md)

---

**🎉 Система готова к развертыванию!**
