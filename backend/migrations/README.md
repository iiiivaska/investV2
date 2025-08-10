# 🗄️ Директория миграций

Эта директория содержит все файлы, связанные с управлением миграциями базы данных в проекте InvestV2.

## 📂 Структура

```
migrations/
├── alembic/                    # Основная директория Alembic
│   ├── versions/              # Файлы миграций
│   │   ├── 6cde36e9a795_*.py  # Первая миграция (users table)
│   │   └── 1581fdc380d1_*.py  # Вторая миграция (phone field)
│   ├── env.py                 # Настройки окружения Alembic
│   ├── README                 # Документация Alembic
│   └── script.py.mako        # Шаблон для генерации миграций
├── alembic.ini               # Конфигурация Alembic
├── migrate.py                # Утилита для управления миграциями
├── investv2.db              # SQLite база данных (для разработки)
├── ALEMBIC_GUIDE.md         # Подробное руководство по миграциям
├── ALEMBIC_EXAMPLES.md      # Примеры использования
└── README.md                # Этот файл
```

## 🚀 Использование

### Из корня проекта (рекомендуется):
```bash
cd backend
source venv/bin/activate

# Проверить статус
python migrate.py status

# Создать миграцию
python migrate.py create "Описание изменений"

# Применить миграции
python migrate.py upgrade

# Откатить миграцию
python migrate.py downgrade
```

### Из директории migrations:
```bash
cd backend/migrations
source ../venv/bin/activate

# Прямые команды Alembic
alembic current
alembic revision --autogenerate -m "Описание"
alembic upgrade head
alembic downgrade -1
```

## 📊 Текущее состояние

- ✅ **База данных**: SQLite (`investv2.db`)
- ✅ **Таблица users**: Создана с полями id, email, hashed_password, first_name, last_name, is_active, is_verified, is_superuser, last_login, created_at, updated_at, phone
- ✅ **Миграции**: 2 миграции применены
- ✅ **Статус**: Все миграции актуальны

## 🔧 Конфигурация

### База данных
- **Разработка**: SQLite (`investv2.db`)
- **Production**: PostgreSQL (настраивается в `app/core/config.py`)

### Пути
- **Конфигурация**: `alembic.ini` → `script_location = %(here)s/alembic`
- **Модели**: Импортируются из `app/models/`
- **Настройки**: Получаются из `app/core/config.py`

## 📚 Документация

- 📖 [Подробное руководство](ALEMBIC_GUIDE.md)
- 🎯 [Примеры использования](ALEMBIC_EXAMPLES.md)
- 🔗 [Официальная документация Alembic](https://alembic.sqlalchemy.org/)

## 🛠️ Разработка

### Добавление новых моделей:
1. Создайте модель в `app/models/`
2. Импортируйте в `app/models/__init__.py`
3. Добавьте импорт в `alembic/env.py`
4. Создайте миграцию: `python migrate.py create "Add new model"`

### Изменение существующих моделей:
1. Измените модель в `app/models/`
2. Создайте миграцию: `python migrate.py create "Change model"`
3. Проверьте сгенерированную миграцию
4. Примените: `python migrate.py upgrade`

## 🔍 Диагностика

### Проверка статуса:
```bash
python migrate.py status
```

### Просмотр SQL без выполнения:
```bash
cd migrations
alembic upgrade head --sql
```

### Сброс миграций:
```bash
cd migrations
alembic stamp head
```

## ⚠️ Важные замечания

1. **Всегда проверяйте** сгенерированные миграции перед применением
2. **Делайте бэкапы** перед применением миграций в production
3. **Тестируйте миграции** на копии данных
4. **Не изменяйте** уже примененные миграции

---

**🎉 Миграции готовы к использованию!**
