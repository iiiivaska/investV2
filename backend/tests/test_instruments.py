from __future__ import annotations

import sys
import types
from typing import List


class DummyAccount:
    def __init__(self, id: str, name: str | None = None):
        self.id = id
        self.name = name
        self.type = "brokerage"
        self.status = "open"
        self.opened_date = None
        self.closed_date = None


class DummyServices:
    class Users:
        @staticmethod
        def get_accounts():
            class Resp:
                accounts: List[DummyAccount] = [DummyAccount("acc-1", "Main")]  # type: ignore[assignment]

            return Resp()

    users = Users()


class DummyClient:
    def __init__(self, token: str):
        self.token = token

    def __enter__(self):
        return DummyServices()

    def __exit__(self, exc_type, exc, tb):
        return None


def register_and_login(test_client):
    import uuid

    unique_id = str(uuid.uuid4())[:8]
    email = f"test_{unique_id}@example.com"

    test_client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "password": "secret",
            "first_name": "Test",
            "last_name": "User",
        },
    )
    r = test_client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": "secret"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    tokens = r.json()
    return tokens["access_token"]


def test_instruments_hello(test_client):
    r = test_client.get("/api/v1/instruments/hello")
    assert r.status_code == 200


def test_tinkoff_demo_with_monkeypatch(test_client, monkeypatch):
    # Provide fake SDK module so that `from tinkoff.invest import Client` works
    fake_invest_module = types.ModuleType("tinkoff.invest")

    class FakeBaseClient:
        def __init__(self, token: str):
            self.token = token

        def __enter__(self):
            return DummyServices()

        def __exit__(self, exc_type, exc, tb):
            return None

    fake_invest_module.Client = FakeBaseClient  # type: ignore[attr-defined]
    fake_tinkoff_pkg = types.ModuleType("tinkoff")
    fake_tinkoff_pkg.invest = fake_invest_module  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "tinkoff", fake_tinkoff_pkg)
    monkeypatch.setitem(sys.modules, "tinkoff.invest", fake_invest_module)

    access_token = register_and_login(test_client)

    # Set tinkoff token
    r = test_client.post(
        "/api/v1/users/tinkoff-token",
        json={"tinkoff_api_token": "FAKE"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert r.status_code == 204

    r = test_client.get(
        "/api/v1/instruments/tinkoff-demo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["source"] == "tinkoff"
    assert data["endpoint"] == "users.get_accounts"
    assert isinstance(data["accounts"], list)
