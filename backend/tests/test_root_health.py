from __future__ import annotations


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert data["message"].startswith("Hello World")


def test_health(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
