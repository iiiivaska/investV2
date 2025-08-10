# 📈 InvestV2

![CI](https://github.com/ваш-username/investV2/actions/workflows/ci.yml/badge.svg)

Серверное приложение для управления инвестиционным портфелем с интеграцией Tinkoff Invest API.

## 🎯 Описание

InvestV2 — это современное FastAPI приложение для управления инвестиционным портфелем, которое предоставляет:

- ✅ **REST API** для мобильных и веб-клиентов
- ✅ **Интеграцию с Tinkoff Invest API** для получения рыночных данных
- ✅ **Систему авторизации** с JWT токенами
- ✅ **Аналитику портфеля** и отчеты
- ✅ **Безопасное хранение данных** в PostgreSQL
- ✅ **Простая конфигурация** с PostgreSQL по умолчанию

## 🚀 Быстрый старт

```bash
# Клонируйте репозиторий
git clone https://github.com/ваш-username/investV2.git
cd investV2

# Перейдите в backend и запустите приложение
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run_dev.py
```

Приложение будет доступно по адресу: **http://localhost:8000/**

## 📚 Документация

- **API документация**: http://localhost:8000/docs
- **Альтернативная документация**: http://localhost:8000/redoc
- **Архитектура**: [.cursor/architecture.mdс](.cursor/architecture.mdс)
- **Структура проекта**: [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)
- **Руководство backend**: [backend/README.md](backend/README.md)
- **PostgreSQL настройка**: [backend/postgres/README.md](backend/postgres/README.md)
 - **TInvest_Engine сервис**: [backend/app/TInvest_Engine/README.md](backend/app/TInvest_Engine/README.md)

## 🏗️ Архитектура

```
investV2/
├── backend/              # FastAPI серверное приложение
│   ├── app/             # Основной код приложения
│   │   ├── api/v1/      # API endpoints
│   │   ├── models/      # SQLAlchemy модели
│   │   ├── schemas/     # Pydantic схемы
│   │   └── core/        # Конфигурация
│   ├── postgres/        # PostgreSQL утилиты
│   │   ├── init_postgres.py
│   │   ├── switch_db.py
│   │   └── POSTGRESQL_SETUP.md
│   ├── requirements.txt # Зависимости
│   └── docker-compose.yml # Docker настройки
└── .cursor/             # Документация и архитектура
```

## 🔧 Технологии

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **База данных**: PostgreSQL + Redis
- **Контейнеризация**: Docker, Docker Compose
- **API**: REST + автодокументация OpenAPI/Swagger
- **Авторизация**: JWT токены + bcrypt

## 🗄️ База данных

### PostgreSQL (обязательно)

Проект использует PostgreSQL как основную базу данных для всех сред (разработка, тестирование, production).

### Настройка PostgreSQL

```bash
# Создание пользователя и БД
psql postgres -c "CREATE USER investv2 WITH PASSWORD 'password' CREATEDB;"
psql postgres -c "CREATE DATABASE investv2 OWNER investv2;"

# Инициализация и миграции
python3 postgres/init_postgres.py
python3 migrate.py upgrade
```

### Проверка статуса

```bash
# Проверка статуса
python3 postgres/switch_db.py status

# Проверка подключения
python3 postgres/switch_db.py check
```

📖 **Подробное руководство**: [backend/postgres/POSTGRESQL_SETUP.md](backend/postgres/POSTGRESQL_SETUP.md)

## 📡 API Endpoints

### Базовые
- `GET /` - Hello World + информация об API
- `GET /health` - Health check

### Модули API v1
- `GET /api/v1/auth/hello` - Аутентификация
- `POST /api/v1/auth/register` - Регистрация
- `POST /api/v1/auth/login` - Вход (OAuth2 Password)
- `POST /api/v1/auth/refresh` - Обновление токенов
- `POST /api/v1/auth/logout` - Выход
- `GET /api/v1/users/hello` - Управление пользователями
- `GET /api/v1/users/me` - Текущий пользователь (Bearer)
- `POST /api/v1/users/tinkoff-token` - Сохранить персональный Tinkoff токен пользователю (Bearer)
- `GET /api/v1/portfolio/hello` - Портфель пользователя
- `GET /api/v1/instruments/hello` - Финансовые инструменты
- `GET /api/v1/analytics/hello` - Аналитика и отчеты
 - `GET /api/v1/instruments/tinkoff-demo` - Демонстрация вызова Tinkoff Invest API (Bearer)

*Все endpoints возвращают JSON и готовы для разработки.*

## ✅ CI (GitHub Actions)

- Автоматический запуск `pytest` на каждый push и pull request.
- Ветка `main` должна мержиться только с зелёным статусом CI.

Как включить обязательное прохождение тестов:
- В настройках репозитория → Branches → Add branch protection rule → Включить “Require status checks to pass before merging” и выбрать джобу `tests (pytest)`.

## 🐳 Docker

```bash
# Запуск с Docker (требует Docker Desktop)
cd backend
docker-compose up --build
```

Включает:
- FastAPI приложение (порт 8000)
- PostgreSQL (порт 5432)
- Redis (порт 6379)
- pgAdmin (порт 5050)

## 🔐 Безопасность

- JWT токены для аутентификации (OAuth2 password flow)
- bcrypt для хеширования паролей
- CORS настройки
- Валидация данных через Pydantic
- Изоляция данных пользователей

## 📋 Roadmap

### ✅ Фаза 1: MVP (готово)
- [x] Базовая структура FastAPI
- [x] API endpoints с Hello World
- [x] Docker конфигурация
- [x] Документация

### ✅ Фаза 2: Core функциональность (готово)
- [x] Система миграций Alembic
- [x] База данных (PostgreSQL)
- [x] Организованная структура PostgreSQL утилит
- [x] Упрощенная конфигурация (только PostgreSQL)
- [x] JWT аутентификация
- [ ] Базовые CRUD операции
- [x] Интеграция с Tinkoff API

### 🚀 Фаза 3: Расширенные возможности
- [ ] Аналитика портфеля
- [ ] Уведомления
- [ ] Отчеты и экспорт
- [ ] Мобильное приложение

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/новая-функция`)
3. Зафиксируйте изменения (`git commit -m 'Добавить новую функцию'`)
4. Пушьте в ветку (`git push origin feature/новая-функция`)
5. Откройте Pull Request

## 📄 Лицензия

MIT License. См. [LICENSE](LICENSE) для деталей.

## 🆘 Поддержка

- 📧 Email: ваш-email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/ваш-username/investV2/issues)
- 📖 Wiki: [GitHub Wiki](https://github.com/ваш-username/investV2/wiki)

### Как аутентифицироваться

```bash
# Регистрация пользователя
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"secret"}'

# Логин и получение токенов
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=user@example.com&password=secret'

# Запрос текущего пользователя с Bearer токеном
curl http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer <ACCESS_TOKEN>"

# Установка персонального Tinkoff токена пользователю (используется продовый API)
curl -X POST http://localhost:8000/api/v1/users/tinkoff-token \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"tinkoff_api_token":"<PROD_TINKOFF_TOKEN>"}'

# Демонстрационный вызов Tinkoff Invest API (список аккаунтов)
curl http://localhost:8000/api/v1/instruments/tinkoff-demo \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```
