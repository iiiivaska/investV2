# 🚀 Быстрый старт InvestV2

## ✅ Приложение уже работает!

FastAPI приложение уже запущено и работает. Вы можете протестировать endpoints:

```bash
# Основной Hello World endpoint
curl http://localhost:8000/

# Health check
curl http://localhost:8000/health

# Все модули API
curl http://localhost:8000/api/v1/auth/hello
curl http://localhost:8000/api/v1/users/hello
curl http://localhost:8000/api/v1/portfolio/hello
curl http://localhost:8000/api/v1/instruments/hello
curl http://localhost:8000/api/v1/analytics/hello
```

## 📚 Документация API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🐳 Docker опции

### Опция 1: Без Docker (уже работает)
```bash
cd backend
source venv/bin/activate
python run_dev.py
```

### Опция 2: С Docker (требует запущенный Docker Desktop)
```bash
# Сначала запустите Docker Desktop, затем:
cd backend
docker-compose up --build
```

## 🔧 Исправленные проблемы

✅ Убрал устаревший атрибут `version` из docker-compose.yml  
✅ Все endpoints возвращают корректный JSON  
✅ Приложение запускается и работает стабильно  

## 🗄️ База данных и миграции

База данных уже настроена и готова к работе!

```bash
# Проверить статус миграций
cd backend
source venv/bin/activate
python migrate.py status

# Посмотреть таблицы в БД
sqlite3 migrations/investv2.db ".tables"
```

📖 **Руководство по миграциям**: [migrations/ALEMBIC_GUIDE.md](migrations/ALEMBIC_GUIDE.md)

## 🎯 Следующие шаги

1. **Протестируйте API** - все endpoints работают
2. **Изучите документацию** - откройте /docs в браузере  
3. **Работайте с БД** - используйте Alembic для миграций
4. **Добавьте функциональность** - начните с аутентификации

## ❓ Нужна помощь?

- Проблемы с Docker? → Запустите Docker Desktop первым
- Нужны новые endpoints? → Добавьте в соответствующие модули API
- Хотите базу данных? → Настроим PostgreSQL подключение
