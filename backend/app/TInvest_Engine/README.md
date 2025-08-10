# TInvest_Engine

Сервис для интеграции с Tinkoff Invest API, инкапсулирующий работу с официальным SDK `tinkoff-investments` и предоставляющий удобный интерфейс для использования в приложении.

## Возможности

- Работа с продовым API Tinkoff Invest (`invest-public-api.tinkoff.ru:443`)
- Контекстный клиент-обертка `TInvestClient`
- Демонстрационные методы: получение списка аккаунтов пользователя

## Установка зависимостей

```bash
pip install tinkoff-investments
```

Либо добавьте в `backend/requirements.txt`:

```
tinkoff-investments==0.2.0
```

## Использование

```python
from app.TInvest_Engine.client import TInvestClient

user_token = "<PROD_TOKEN>"
with TInvestClient(user_token) as ti:
    accounts = ti.list_accounts()
    print(accounts)
```

## Безопасность

- Используйте только продовые токены для продового окружения.
- Не храните токены в открытом виде в репозитории. В проекте предусмотрено хранение токена в таблице `users` в поле `tinkoff_api_token`.
- Доступ к демо-методу защищен аутентификацией (Bearer).

## Структура

```
app/TInvest_Engine/
├── __init__.py
├── client.py        # Клиент-обертка над SDK
└── README.md        # Документация сервиса
```

## Демонстрационный эндпоинт

Реализован эндпоинт `GET /api/v1/instruments/tinkoff-demo`, который:
- Берет токен текущего пользователя (`users.tinkoff_api_token`)
- Вызывает метод `users.get_accounts()` Tinkoff Invest API
- Возвращает результат в JSON

Для работы необходимо установить токен пользователю и выполнить запрос под аутентифицированным пользователем.

