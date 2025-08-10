# 🗄️ PostgreSQL для InvestV2

Эта директория содержит все файлы, связанные с настройкой и управлением PostgreSQL для проекта InvestV2.

## 📁 Содержимое директории

### Скрипты управления

- **`init_postgres.py`** - Инициализация PostgreSQL базы данных
  - Создание пользователя и БД
  - Проверка подключения
  - Автоматическая настройка

- **`switch_db.py`** - Проверка статуса PostgreSQL
  - Проверка конфигурации
  - Тестирование подключения
  - Диагностика проблем

### Документация

- **`POSTGRESQL_SETUP.md`** - Подробное руководство по настройке PostgreSQL
  - Установка PostgreSQL
  - Настройка пользователей и БД
  - Управление миграциями
  - Устранение неполадок

## 🚀 Быстрый старт

```bash
# Инициализация базы данных
python3 postgres/init_postgres.py

# Проверка статуса
python3 postgres/switch_db.py status

# Проверка подключения
python3 postgres/switch_db.py check

# Применение миграций
python3 migrate.py upgrade
```

## 📚 Документация

- **Подробное руководство**: [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md)
- **Основной README**: [../README.md](../README.md)
- **Backend README**: [../README.md](../README.md)

## 🔧 Использование

### Проверка статуса PostgreSQL

```bash
# Показать текущий статус
python3 postgres/switch_db.py status

# Проверить подключение
python3 postgres/switch_db.py check
```

### Инициализация PostgreSQL

```bash
# Создание пользователя и БД
psql postgres -c "CREATE USER investv2 WITH PASSWORD 'password' CREATEDB;"
psql postgres -c "CREATE DATABASE investv2 OWNER investv2;"

# Инициализация через скрипт
python3 postgres/init_postgres.py
```

## 🐳 Docker

При использовании Docker Compose PostgreSQL настраивается автоматически:

```bash
# Запуск всех сервисов
docker-compose up --build

# Только PostgreSQL
docker-compose up postgres
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

### Подключение к базе данных

```bash
# Через psql
psql -U investv2 -d investv2

# Через pgAdmin (при использовании Docker)
# http://localhost:5050
```

## 🚨 Устранение неполадок

См. [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) для подробного руководства по устранению неполадок.

### Частые проблемы

1. **"role 'investv2' does not exist"**
   ```bash
   psql postgres -c "CREATE USER investv2 WITH PASSWORD 'password' CREATEDB;"
   ```

2. **"database 'investv2' does not exist"**
   ```bash
   psql postgres -c "CREATE DATABASE investv2 OWNER investv2;"
   ```

3. **Проблемы с миграциями**
   ```bash
   python3 migrate.py upgrade
   ```

4. **Проверка подключения**
   ```bash
   python3 postgres/switch_db.py check
   ```
