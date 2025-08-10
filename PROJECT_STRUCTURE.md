# 📁 Структура проекта InvestV2

## Созданная структура

```
investV2/
├── backend/                          # FastAPI серверное приложение
│   ├── app/                          # Основной код приложения
│   │   ├── __init__.py              
│   │   ├── main.py                   # 🚀 Точка входа FastAPI
│   │   │
│   │   ├── api/                      # API endpoints
│   │   │   ├── __init__.py
│   │   │   └── v1/                   # API версия 1
│   │   │       ├── __init__.py
│   │   │       ├── auth.py           # 🔐 Авторизация (/api/v1/auth/*)
│   │   │       ├── users.py          # 👤 Пользователи (/api/v1/users/*)
│   │   │       ├── portfolio.py      # 💼 Портфель (/api/v1/portfolio/*)
│   │   │       ├── instruments.py    # 📈 Инструменты (/api/v1/instruments/*)
│   │   │       └── analytics.py      # 📊 Аналитика (/api/v1/analytics/*)
│   │   │
│   │   ├── core/                     # Основная конфигурация
│   │   │   ├── __init__.py
│   │   │   └── config.py             # ⚙️ Настройки приложения
│   │   │
│   │   ├── database/                 # Настройки БД
│   │   │   ├── __init__.py
│   │   │   └── database.py           # 🗄️ Подключение к PostgreSQL
│   │   │
│   │   ├── models/                   # SQLAlchemy модели
│   │   │   ├── __init__.py
│   │   │   ├── base.py               # Базовая модель
│   │   │   └── user.py               # Модель пользователя
│   │   │
│   │   └── schemas/                  # Pydantic схемы
│   │       ├── __init__.py
│   │       ├── auth.py               # Схемы авторизации
│   │       └── user.py               # Схемы пользователя
│   │
│   ├── postgres/                     # 🗄️ PostgreSQL утилиты
│   │   ├── __init__.py
│   │   ├── init_postgres.py          # 🔧 Инициализация PostgreSQL
│   │   ├── switch_db.py              # 🔍 Проверка статуса
│   │   ├── POSTGRESQL_SETUP.md       # 📖 Подробное руководство
│   │   ├── README.md                 # 📚 Документация PostgreSQL
│   │   └── CHANGELOG.md              # 📝 История изменений
│   │
│   ├── migrations/                   # 🗄️ Все файлы миграций
│   │   ├── alembic/                 # Основная директория Alembic
│   │   │   ├── versions/           # Файлы миграций
│   │   │   ├── env.py              # Настройки окружения
│   │   │   └── script.py.mako     # Шаблон миграций
│   │   ├── alembic.ini             # ⚙️ Конфигурация Alembic
│   │   ├── migrate.py              # 🛠️ Утилита управления
│   │   ├── ALEMBIC_GUIDE.md        # 📖 Подробное руководство
│   │   ├── ALEMBIC_EXAMPLES.md     # 🎯 Примеры использования
│   │   └── README.md               # 📚 Документация миграций
│   ├── venv/                         # Виртуальное окружение Python
│   ├── requirements.txt              # 📦 Зависимости Python
│   ├── env.example                   # 🔧 Пример переменных окружения
│   ├── run_dev.py                    # 🏃 Скрипт запуска для разработки
│   ├── migrate.py                    # 🛠️ Утилита управления миграциями
│   ├── Dockerfile                    # 🐳 Docker образ
│   ├── docker-compose.yml           # 🐳 Композиция сервисов
│   ├── .dockerignore                # 🐳 Игнорируемые Docker файлы
│   └── README.md                     # 📚 Документация бэкенда
│
├── .cursor/                          # Конфигурация Cursor IDE
│   ├── main.mdc                     # Основная документация
│   └── architecture.mdс             # Архитектурная документация
│
└── PROJECT_STRUCTURE.md             # 📋 Этот файл
```

## 🚀 Рабочие endpoints

### Основные
- `GET /` - Hello World с информацией об API
- `GET /health` - Health check

### API v1 модули (все с Hello World endpoints)
- `GET /api/v1/auth/hello` - Модуль аутентификации
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход (OAuth2, form: username, password)
- `POST /api/v1/auth/refresh` - Обновление токенов
- `POST /api/v1/auth/logout` - Выход
- `GET /api/v1/users/hello` - Модуль пользователей
- `GET /api/v1/users/me` - Текущий пользователь (Bearer)
- `GET /api/v1/portfolio/hello` - Модуль портфеля
- `GET /api/v1/instruments/hello` - Модуль инструментов
- `GET /api/v1/analytics/hello` - Модуль аналитики

### Документация API
- `GET /docs` - Swagger UI документация
- `GET /redoc` - ReDoc документация

## ✅ Что работает

1. ✅ **FastAPI приложение** запускается и работает
2. ✅ **Все endpoints** возвращают JSON ответы
3. ✅ **Структура проекта** соответствует архитектуре
4. ✅ **Модульная архитектура** с разделением по функциональности
5. ✅ **Настройки** через Pydantic Settings
6. ✅ **SQLAlchemy модели** готовы для БД
7. ✅ **Pydantic схемы** для валидации
8. ✅ **Docker конфигурация** для deployment
9. ✅ **CORS настройки** для кросс-доменных запросов
10. ✅ **JWT аутентификация** (регистрация, вход, refresh, logout, /users/me)
11. ✅ **Alembic миграции** настроены и работают
12. ✅ **PostgreSQL** полностью настроен и работает
13. ✅ **Организованная структура** PostgreSQL утилит
14. ✅ **Упрощенная конфигурация** (только PostgreSQL)

## 🎯 Следующие шаги

- [x] Настройка Alembic для миграций БД
- [x] Подключение к PostgreSQL
- [x] Организация PostgreSQL утилит в отдельную директорию
- [x] Упрощение конфигурации (только PostgreSQL)
- [x] Реализация JWT аутентификации
- [ ] Интеграция с Tinkoff Invest API
- [ ] Добавление тестов
- [ ] Настройка CI/CD pipeline

## 🚀 Как запустить

### Быстрый запуск
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_dev.py
```

### С Docker
```bash
cd backend
docker-compose up --build
```

### Настройка PostgreSQL
```bash
cd backend
# Инициализация базы данных
python3 postgres/init_postgres.py

# Проверка подключения
python3 postgres/switch_db.py check

# Применение миграций
python3 migrate.py upgrade
```

### Примеры аутентификации

```bash
# Регистрация
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"secret"}'

# Логин (OAuth2 Password)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=secret'

# Обращение к защищенному endpoint
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

Приложение будет доступно по адресу: http://localhost:8000/
