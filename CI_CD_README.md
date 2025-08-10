# 🚀 CI/CD Pipeline для InvestV2

## 📋 Обзор

Проект использует GitHub Actions для автоматизации процессов разработки, тестирования и развертывания.

## 🔧 Настройка

### Предварительные требования

1. **GitHub репозиторий** с настроенными секретами
2. **Python 3.11+** для локальной разработки
3. **Docker** для контейнеризации

### Переменные окружения

Создайте следующие секреты в настройках GitHub репозитория:

- `DOCKER_USERNAME` - имя пользователя Docker Hub
- `DOCKER_PASSWORD` - пароль Docker Hub
- `CODECOV_TOKEN` - токен для Codecov (опционально)

## 🏃‍♂️ Workflow

### 1. Test Job

**Триггеры:**
- Push в `main` и `develop` ветки
- Pull Request в `main` и `develop` ветки

**Что выполняется:**
- ✅ Установка зависимостей
- ✅ Линтинг кода (flake8, black, isort)
- ✅ Запуск тестов с покрытием
- ✅ Загрузка отчета покрытия в Codecov

**Сервисы:**
- PostgreSQL 15 для тестов
- Redis 7 для кеширования

### 2. Security Job

**Триггеры:**
- После успешного выполнения Test Job

**Что выполняется:**
- ✅ Проверка безопасности с Bandit
- ✅ Проверка уязвимостей зависимостей с Safety
- ✅ Загрузка отчетов безопасности как артефакты

### 3. Build Job

**Триггеры:**
- Push в `main` ветку (только)

**Что выполняется:**
- ✅ Сборка Docker образа
- ✅ Загрузка образа как артефакт

## 🧪 Тестирование

### Запуск тестов локально

```bash
cd backend

# Установка зависимостей
pip install -r requirements.txt

# Запуск всех тестов
pytest tests/ -v

# Запуск с покрытием
pytest tests/ -v --cov=app --cov-report=term-missing

# Запуск конкретного теста
pytest tests/test_auth_users.py::test_auth_flow_and_users_me -v
```

### Тесты в CI

В CI среде тесты запускаются с PostgreSQL базой данных:

```yaml
DATABASE_URL: postgresql://investv2:password@localhost:5432/investv2_test
REDIS_URL: redis://localhost:6379/0
SECRET_KEY: test-secret-key-for-ci
```

### Покрытие кода

Минимальное покрытие: **70%**

Отчеты покрытия:
- Терминал: `--cov-report=term-missing`
- XML: `--cov-report=xml` (для Codecov)

## 🔍 Линтинг

### Инструменты

- **flake8** - проверка стиля кода
- **black** - форматирование кода
- **isort** - сортировка импортов

### Конфигурация

- Максимальная длина строки: 88 символов
- Игнорируемые ошибки: E203, W503, E501
- Исключения: миграции, виртуальные окружения

### Запуск локально

```bash
cd backend

# Проверка стиля
flake8 app tests

# Форматирование
black app tests

# Сортировка импортов
isort app tests
```

## 🔒 Безопасность

### Инструменты

- **Bandit** - статический анализ безопасности
- **Safety** - проверка уязвимостей зависимостей

### Конфигурация

- Исключения: тесты, миграции
- Пропускаемые проверки: B101, B601

### Запуск локально

```bash
cd backend

# Проверка безопасности
bandit -r app -f json -o bandit-report.json

# Проверка зависимостей
safety check --json --output safety-report.json
```

## 📊 Отчеты

### Codecov

Отчеты покрытия автоматически загружаются в Codecov при каждом PR и push в main.

### Артефакты

Следующие артефакты сохраняются:
- Отчеты безопасности (Bandit, Safety)
- Docker образ (при push в main)

## 🚨 Устранение неполадок

### Тесты не проходят

1. Проверьте логи в GitHub Actions
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию базы данных

### Проблемы с линтингом

1. Запустите `black app tests` для форматирования
2. Запустите `isort app tests` для сортировки импортов
3. Исправьте ошибки flake8

### Проблемы с безопасностью

1. Проверьте отчеты Bandit и Safety
2. Обновите уязвимые зависимости
3. Исправьте проблемы безопасности в коде

## 📈 Метрики

### Покрытие кода

Текущее покрытие: [Codecov Badge]

### Статус сборки

![CI/CD Status](https://github.com/{owner}/{repo}/workflows/CI%2FCD%20Pipeline/badge.svg)

## 🔄 Обновление

Для обновления CI/CD pipeline:

1. Отредактируйте `.github/workflows/ci.yml`
2. Протестируйте изменения локально
3. Создайте Pull Request
4. Проверьте, что все тесты проходят

## 📚 Полезные ссылки

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Pytest Documentation](https://docs.pytest.org/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [Codecov Documentation](https://docs.codecov.io/)
