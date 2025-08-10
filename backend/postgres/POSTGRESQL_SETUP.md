# 🗄️ Настройка PostgreSQL для InvestV2

Это руководство поможет настроить PostgreSQL для проекта InvestV2.

## 📋 Предварительные требования

- PostgreSQL 12+ установлен и запущен
- Python 3.11+ с виртуальным окружением
- Все зависимости установлены

## 🚀 Быстрая настройка

### 1. Установка PostgreSQL

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

### 2. Создание пользователя и базы данных

```bash
# Создание пользователя
psql postgres -c "CREATE USER investv2 WITH PASSWORD 'password' CREATEDB;"

# Создание базы данных
psql postgres -c "CREATE DATABASE investv2 OWNER investv2;"
```

### 3. Настройка проекта

```bash
# Переключение на PostgreSQL
python3 switch_db.py postgres

# Инициализация базы данных
python3 init_postgres.py

# Применение миграций
python3 migrate.py upgrade
```

### 4. Запуск приложения

```bash
python3 run_dev.py
```

## 🔧 Управление базой данных

### Переключение между SQLite и PostgreSQL

```bash
# Переключение на SQLite (для разработки)
python3 switch_db.py sqlite

# Переключение на PostgreSQL (для production)
python3 switch_db.py postgres

# Проверка текущей БД
python3 switch_db.py status
```

### Управление миграциями

```bash
# Просмотр статуса
python3 migrate.py status

# Применение миграций
python3 migrate.py upgrade

# Откат миграции
python3 migrate.py downgrade

# Создание новой миграции
python3 migrate.py create "Описание изменений"
```

### Прямые команды Alembic

```bash
cd migrations

# Создание миграции
alembic revision --autogenerate -m "Описание"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1

# Просмотр истории
alembic history --verbose
```

## 🐳 Docker

### Запуск с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up --build

# Только база данных
docker-compose up postgres redis
```

### Доступные сервисы

- **FastAPI**: http://localhost:8000
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **pgAdmin**: http://localhost:5050

## 🔍 Проверка подключения

### Проверка через psql

```bash
# Подключение к базе данных
psql -U investv2 -d investv2

# Просмотр таблиц
\dt

# Просмотр структуры таблицы
\d users

# Выход
\q
```

### Проверка через Python

```bash
python3 -c "
from app.database.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text('SELECT version();'))
    print('PostgreSQL version:', result.fetchone()[0])
"
```

## 🚨 Устранение неполадок

### Проблема: "role 'investv2' does not exist"

```bash
# Создание пользователя
psql postgres -c "CREATE USER investv2 WITH PASSWORD 'password' CREATEDB;"
```

### Проблема: "database 'investv2' does not exist"

```bash
# Создание базы данных
psql postgres -c "CREATE DATABASE investv2 OWNER investv2;"
```

### Проблема: "Can't locate revision identified by '1581fdc380d1'"

```bash
# Удаление SQLite файла
rm -f migrations/investv2.db

# Пересоздание миграций
rm -rf migrations/alembic
cd migrations && alembic init alembic
cd .. && python3 migrate.py create "Initial migration"
```

### Проблема: "psycopg2 not found"

```bash
# Установка psycopg2
pip install psycopg2-binary

# Или для Python 3.13+
pip install psycopg2-binary --upgrade
```

## 📊 Мониторинг

### Проверка статуса PostgreSQL

```bash
# macOS
brew services list | grep postgresql

# Ubuntu
sudo systemctl status postgresql

# Проверка подключений
psql -U investv2 -d investv2 -c "SELECT count(*) FROM pg_stat_activity;"
```

### Логи PostgreSQL

```bash
# macOS
tail -f /opt/homebrew/var/log/postgresql@14.log

# Ubuntu
sudo tail -f /var/log/postgresql/postgresql-*.log
```

## 🔐 Безопасность

### Рекомендации для production

1. **Измените пароль по умолчанию:**
   ```sql
   ALTER USER investv2 WITH PASSWORD 'strong_password';
   ```

2. **Ограничьте доступ:**
   ```sql
   REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;
   GRANT ALL ON ALL TABLES IN SCHEMA public TO investv2;
   ```

3. **Настройте SSL:**
   ```bash
   # В postgresql.conf
   ssl = on
   ssl_cert_file = 'server.crt'
   ssl_key_file = 'server.key'
   ```

4. **Используйте переменные окружения:**
   ```bash
   export POSTGRES_PASSWORD="your_secure_password"
   ```

## 📚 Дополнительные ресурсы

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
