# InvestV2 Backend API

Серверное приложение для управления инвестиционным портфелем с интеграцией Tinkoff Invest API.

## 🚀 Быстрый старт

### Локальная разработка с Docker

1. **Клонируйте репозиторий**
   ```bash
   git clone <your-repo-url>
   cd investV2/backend
   ```

2. **Запустите приложение с Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Проверьте работу API**
   - Основной endpoint: http://localhost:8000/
   - Документация API: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc
   - Health check: http://localhost:8000/health

### Ручная установка

1. **Установите зависимости**
   ```bash
   pip install -r requirements.txt
   ```

2. **Настройте переменные окружения**
   ```bash
   cp env.example .env
   # Отредактируйте .env файл с вашими настройками
   ```

3. **Запустите приложение**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## 📁 Структура проекта

```
backend/
├── app/
│   ├── api/v1/           # API endpoints
│   ├── core/             # Основная конфигурация
│   ├── database/         # Настройки БД
│   ├── models/           # SQLAlchemy модели
│   ├── schemas/          # Pydantic схемы
│   └── main.py           # Точка входа
├── alembic/              # Миграции БД
├── tests/                # Тесты
├── requirements.txt      # Зависимости
├── Dockerfile           # Docker образ
└── docker-compose.yml   # Локальная разработка
```

## 🔧 Доступные API endpoints

### Базовые endpoints
- `GET /` - Hello World с информацией об API
- `GET /health` - Health check

### Модули API (v1)
- `/api/v1/auth/hello` - Аутентификация
- `/api/v1/users/hello` - Управление пользователями
- `/api/v1/portfolio/hello` - Портфель пользователя
- `/api/v1/instruments/hello` - Финансовые инструменты
- `/api/v1/analytics/hello` - Аналитика

## 🗄️ База данных

Проект использует PostgreSQL как основную базу данных и Redis для кеширования.

При запуске через Docker Compose автоматически создаются:
- PostgreSQL (порт 5432)
- Redis (порт 6379)
- pgAdmin (порт 5050) - admin@investv2.com/admin

## 🔒 Безопасность

- JWT токены для аутентификации
- bcrypt для хеширования паролей
- CORS настройки
- Валидация данных через Pydantic

## 🛠️ Разработка

### Установка dev зависимостей
```bash
pip install black isort flake8 mypy pytest
```

### Форматирование кода
```bash
black app/
isort app/
```

### Линтинг
```bash
flake8 app/
mypy app/
```

### Тестирование
```bash
pytest
```

## 🗄️ Миграции базы данных

Проект использует Alembic для управления миграциями базы данных.

### Основные команды:
```bash
# Удобная утилита (рекомендуется)
python migrate.py status           # Статус миграций
python migrate.py upgrade          # Применить миграции
python migrate.py create "Описание" # Создать миграцию

# Прямые команды Alembic (из директории migrations)
cd migrations
alembic revision --autogenerate -m "Описание изменений"
alembic upgrade head
alembic current
alembic downgrade -1
```

📖 **Подробное руководство**: [migrations/ALEMBIC_GUIDE.md](migrations/ALEMBIC_GUIDE.md)



## 📋 TODO

- [x] Настройка Alembic миграций
- [ ] Реализация JWT аутентификации
- [ ] Интеграция с Tinkoff API
- [ ] Добавление тестов
- [ ] Настройка CI/CD

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Зафиксируйте изменения (`git commit -m 'Add amazing feature'`)
4. Пушьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request
