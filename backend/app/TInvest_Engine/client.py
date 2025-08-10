"""
Клиент-обертка для Tinkoff Invest API (production).

Предоставляет высокоуровневые методы для выполнения типовых операций
через официальный SDK `tinkoff-investments`.
"""
from __future__ import annotations

from contextlib import AbstractContextManager
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TinkoffAccount:
    id: str
    name: Optional[str]
    type: str
    status: str
    opened_date: Optional[str]
    closed_date: Optional[str]


class TInvestClient(AbstractContextManager["TInvestClient"]):
    """Контекстный клиент для работы с Tinkoff Invest API.

    Создает и закрывает соединение с API автоматически через контекстный менеджер.
    """

    def __init__(self, token: str) -> None:
        self._token = token
        self._base_client = None  # базовый контекстный менеджер Client
        self._services = None  # объект сервисов, возвращаемый __enter__

    def __enter__(self) -> "TInvestClient":  # type: ignore[override]
        from tinkoff.invest import Client  # локальный импорт

        # Важно: __enter__ SDK возвращает объект сервисов, а закрывать нужно базовый Client
        self._base_client = Client(self._token)
        self._services = self._base_client.__enter__()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:  # type: ignore[override]
        # Закрываем базовый клиент, а не объект сервисов
        if self._base_client is not None:
            self._base_client.__exit__(exc_type, exc, tb)
            self._base_client = None
            self._services = None

    # High-level methods
    def list_accounts(self) -> List[TinkoffAccount]:
        """Возвращает список аккаунтов пользователя."""
        assert self._services is not None, "Client is not initialized"
        response = self._services.users.get_accounts()
        accounts: List[TinkoffAccount] = []
        for acc in response.accounts:
            accounts.append(
                TinkoffAccount(
                    id=acc.id,
                    name=getattr(acc, "name", None),
                    type=str(acc.type),
                    status=str(acc.status),
                    opened_date=str(getattr(acc, "opened_date", "")),
                    closed_date=str(getattr(acc, "closed_date", "")),
                )
            )
        return accounts
