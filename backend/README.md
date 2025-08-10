# 🚀 InvestV2 Backend

FastAPI серверное приложение для управления инвестиционным портфелем с интеграцией Tinkoff Invest API.

## 📋 Содержание

- [Быстрый старт](#-быстрый-старт)
- [Настройка базы данных](#-настройка-базы-данных)
- [Запуск приложения](#-запуск-приложения)
- [API документация](#-api-документация)
- [Разработка](#-разработка)
- [Docker](#-docker)

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Создание виртуального окружения
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### 2. Настройка переменных окружения

```bash
# Копируем пример конфигурации
cp env.example .env

# Редактируем .env файл под свои нужды
nano .env
```

### 3. Запуск приложения

```bash
# Запуск в режиме разработки
python run_dev.py
```

Приложение будет доступно по адресу: **http://localhost:8000/**

## 🗄️ Настройка базы данных

### PostgreSQL (обязательно)

#### Установка PostgreSQL

**macOS (с Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
Скачайте и установите с [официального сайта](https://www.postgresql.org/download/windows/)

#### Настройка PostgreSQL

```bash
# Инициализация базы данных
python3 postgres/init_postgres.py

# Проверка подключения
python3 postgres/switch_db.py check

# Запуск миграций
python3 migrate.py upgrade
```

#### Проверка подключения

```bash
# Проверка статуса базы данных
python3 postgres/switch_db.py status
```

## 🏃 Запуск приложения

### Режим разработки

```bash
python run_dev.py
```

### Продакшн режим

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### С Docker

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Только база данных
docker-compose up postgres redis
```

## 📚 API документация

После запуска приложения доступна автоматическая документация:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Основные endpoints

- `GET /` - Hello World + информация об API
- `GET /health` - Health check

### API v1 модули

- `GET /api/v1/auth/hello` - Модуль аутентификации
- `GET /api/v1/users/hello` - Модуль пользователей
- `GET /api/v1/portfolio/hello` - Модуль портфеля
- `GET /api/v1/instruments/hello` - Модуль инструментов
- `GET /api/v1/analytics/hello` - Модуль аналитики
 - `GET /api/v1/instruments/tinkoff-demo` - Демонстрация вызова Tinkoff Invest API (Bearer)

## 🔧 Разработка

### Структура проекта

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Конфигурация
│   ├── database/        # Настройки БД
│   ├── models/          # SQLAlchemy модели
│   └── schemas/         # Pydantic схемы
├── migrations/          # Миграции Alembic
├── postgres/            # PostgreSQL утилиты
│   ├── init_postgres.py # Инициализация PostgreSQL
│   ├── switch_db.py     # Проверка статуса
│   └── POSTGRESQL_SETUP.md # Документация
├── requirements.txt     # Зависимости
└── run_dev.py          # Скрипт запуска
```

### Управление миграциями

```bash
# Создание новой миграции
python3 migrate.py revision --autogenerate -m "Описание изменений"

# Применение миграций
python3 migrate.py upgrade

# Откат миграции
python3 migrate.py downgrade

# Просмотр истории миграций
python3 migrate.py history
```

### Проверка статуса PostgreSQL

```bash
# Показать текущий статус
python3 postgres/switch_db.py status

# Проверить подключение
python3 postgres/switch_db.py check
```

## 🐳 Docker

### Запуск с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d

# Остановка сервисов
docker-compose down
```

### Доступные сервисы

- **FastAPI**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **pgAdmin**: http://localhost:5050

### Переменные окружения для Docker

```bash
# Создание .env файла для Docker
cp env.example .env

# Редактирование настроек
nano .env
```

## 🔐 Безопасность

- JWT токены для аутентификации
- bcrypt для хеширования паролей
- CORS настройки
- Валидация данных через Pydantic
- Изоляция данных пользователей

## 📊 Мониторинг

### Health Check

```bash
curl http://localhost:8000/health
```

### Логи

```bash
# Просмотр логов приложения
docker-compose logs api

# Просмотр логов базы данных
docker-compose logs postgres
```

## 🚨 Устранение неполадок

### Проблемы с подключением к PostgreSQL

1. **Проверьте, что PostgreSQL запущен:**
   ```bash
   # macOS
   brew services list | grep postgresql
   
   # Ubuntu
   sudo systemctl status postgresql
   ```

2. **Проверьте настройки подключения:**
   ```bash
   python3 postgres/switch_db.py status
   ```

3. **Инициализируйте базу данных:**
   ```bash
   python3 postgres/init_postgres.py
   ```

### Проблемы с миграциями

1. **Проверьте подключение к БД:**
   ```bash
   python3 migrate.py current
   ```

2. **Сбросьте миграции (только для разработки):**
   ```bash
   python3 migrate.py downgrade base
   python3 migrate.py upgrade
   ```

## 📚 Дополнительная документация

- **PostgreSQL настройка**: [postgres/README.md](postgres/README.md)
- **Подробное руководство**: [postgres/POSTGRESQL_SETUP.md](postgres/POSTGRESQL_SETUP.md)
- **Структура проекта**: [../PROJECT_STRUCTURE.md](../PROJECT_STRUCTURE.md)
 - **TInvest_Engine сервис**: [app/TInvest_Engine/README.md](app/TInvest_Engine/README.md)

## 📝 Лицензия

MIT License
