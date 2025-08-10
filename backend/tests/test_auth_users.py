from __future__ import annotations

from typing import Tuple


def register_user(test_client) -> Tuple[str, str]:
    import uuid

    # Use unique email for each test to avoid conflicts
    unique_id = str(uuid.uuid4())[:8]
    payload = {
        "email": f"user_{unique_id}@example.com",
        "password": "secret",
        "first_name": "Ivan",
        "last_name": "Petrov",
    }
    r = test_client.post("/api/v1/auth/register", json=payload)
    assert r.status_code == 201, f"Registration failed: {r.text}"
    data = r.json()
    assert data["email"] == payload["email"]
    return payload["email"], payload["password"]


def login_user(test_client, email: str, password: str) -> str:
    r = test_client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    return tokens["access_token"], tokens["refresh_token"]


def test_auth_flow_and_users_me(test_client):
    email, password = register_user(test_client)
    access_token, refresh_token = login_user(test_client, email, password)

    # Access protected endpoint /users/me
    r = test_client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert r.status_code == 200
    me = r.json()
    assert me["email"] == email

    # Refresh tokens
    r = test_client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert r.status_code == 200
    new_tokens = r.json()
    assert new_tokens["access_token"]

    # Logout (stateless)
    r = test_client.post("/api/v1/auth/logout")
    assert r.status_code == 200


def test_set_tinkoff_token_and_profile(test_client):
    email, password = register_user(test_client)
    access_token, _ = login_user(test_client, email, password)

    # Update Tinkoff token
    r = test_client.post(
        "/api/v1/users/tinkoff-token",
        json={"tinkoff_api_token": "TEST_TOKEN"},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert r.status_code == 204

    # Check profile
    r = test_client.get(
        "/api/v1/users/profile", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert r.status_code == 200
    profile = r.json()
    assert profile["email"] == email
