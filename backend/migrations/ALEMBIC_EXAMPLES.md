# 🚀 Примеры использования Alembic в InvestV2

## Настройка завершена! ✅

Alembic успешно настроен и готов к работе. Вот что уже сделано:

### ✅ Что настроено:
- ✅ Alembic инициализирован
- ✅ Конфигурация настроена для интеграции с моделями
- ✅ База данных SQLite создана (`investv2.db`)
- ✅ Создана первая миграция для таблицы `users`
- ✅ Миграция применена - таблица создана
- ✅ Утилита `migrate.py` для удобного управления

## 📋 Быстрые команды

```bash
# Переходим в директорию и активируем окружение
cd backend
source venv/bin/activate

# Проверяем статус
python migrate.py status

# Создаем новую миграцию (после изменения моделей)
python migrate.py create "Описание изменений"

# Применяем миграции
python migrate.py upgrade

# Откатываем миграцию
python migrate.py downgrade
```

## 🧪 Демонстрация работы

### 1. Текущие таблицы в БД:
```bash
sqlite3 investv2.db ".tables"
# Результат: alembic_version  users
```

### 2. Структура таблицы users:
```sql
CREATE TABLE users (
    id INTEGER NOT NULL, 
    email VARCHAR(255) NOT NULL, 
    hashed_password VARCHAR(255) NOT NULL, 
    first_name VARCHAR(100), 
    last_name VARCHAR(100), 
    is_active BOOLEAN NOT NULL, 
    is_verified BOOLEAN NOT NULL, 
    is_superuser BOOLEAN NOT NULL, 
    last_login DATETIME, 
    created_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
    updated_at DATETIME DEFAULT (CURRENT_TIMESTAMP) NOT NULL, 
    PRIMARY KEY (id)
);
```

### 3. История миграций:
```bash
python migrate.py status
```

## 🔄 Пример добавления нового поля

### Шаг 1: Изменяем модель
```python
# В app/models/user.py добавляем поле
class User(Base):
    # ... существующие поля ...
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
```

### Шаг 2: Создаем миграцию
```bash
python migrate.py create "Add phone field to users"
```

### Шаг 3: Проверяем созданную миграцию
```python
# В файле alembic/versions/xxxxx_add_phone_field_to_users.py
def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))

def downgrade() -> None:
    op.drop_column('users', 'phone')
```

### Шаг 4: Применяем миграцию
```bash
python migrate.py upgrade
```

### Шаг 5: Проверяем результат
```bash
sqlite3 investv2.db ".schema users"
# Поле phone должно появиться в таблице
```

## 🏗️ Добавление новых моделей

### 1. Создаем новую модель
```python
# app/models/portfolio.py
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="portfolios")
```

### 2. Обновляем модель User
```python
# app/models/user.py
class User(Base):
    # ... существующие поля ...
    
    # Связи
    portfolios: Mapped[list["Portfolio"]] = relationship("Portfolio", back_populates="user")
```

### 3. Импортируем в __init__.py
```python
# app/models/__init__.py
from .user import User
from .portfolio import Portfolio

__all__ = ["User", "Portfolio"]
```

### 4. Обновляем env.py
```python
# alembic/env.py
from app.models import user, portfolio  # Добавляем импорт
```

### 5. Создаем миграцию
```bash
python migrate.py create "Add portfolio model"
```

## 📊 Переключение на PostgreSQL

### 1. Обновляем настройки
```python
# app/core/config.py
database_url: str = "postgresql://investv2:password@localhost:5432/investv2"
```

### 2. Устанавливаем драйвер
```bash
pip install psycopg2-binary
```

### 3. Создаем БД PostgreSQL
```sql
CREATE DATABASE investv2;
CREATE USER investv2 WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE investv2 TO investv2;
```

### 4. Применяем миграции
```bash
python migrate.py upgrade
```

## 🛠️ Продвинутые миграции

### Миграция данных
```python
def upgrade() -> None:
    # Создаем таблицу
    op.create_table('categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False)
    )
    
    # Добавляем данные
    from sqlalchemy.sql import table, column
    categories_table = table('categories',
        column('name', sa.String)
    )
    
    op.bulk_insert(categories_table, [
        {'name': 'Акции'},
        {'name': 'Облигации'},
        {'name': 'ETF'}
    ])
```

### Условная миграция
```python
def upgrade() -> None:
    connection = op.get_bind()
    
    # Проверяем существование таблицы
    if not connection.dialect.has_table(connection, 'new_table'):
        op.create_table('new_table',
            sa.Column('id', sa.Integer, primary_key=True)
        )
```

## 🔍 Диагностика проблем

### Проверка статуса
```bash
python migrate.py status
alembic history --verbose
alembic current --verbose
```

### Просмотр SQL без выполнения
```bash
alembic upgrade head --sql
```

### Сброс до определенной ревизии
```bash
alembic stamp head  # Если база синхронизирована вручную
```

## 🎯 Следующие шаги

1. **Добавить новые модели**: Portfolio, Investment, Transaction
2. **Настроить связи между моделями**
3. **Создать seed-данные через миграции**
4. **Переключиться на PostgreSQL для production**
5. **Добавить индексы для оптимизации**

## 📚 Полезные ссылки

- 📖 [Подробное руководство](ALEMBIC_GUIDE.md)
- 📘 [Документация Alembic](https://alembic.sqlalchemy.org/)
- 🔧 [SQLAlchemy модели](https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html)

---

**🎉 Alembic успешно настроен и готов к использованию!**
