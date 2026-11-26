from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "User Service"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice Johnson"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404


def test_get_all_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) >= 3


def test_filter_active_users():
    response = client.get("/users?active=true")
    assert response.status_code == 200
    assert all(user["active"] for user in response.json())


def test_filter_inactive_users():
    response = client.get("/users?active=false")
    assert response.status_code == 200
    assert all(not user["active"] for user in response.json())


def test_create_and_delete_user():
    created = client.post("/users", json={"name": "Test User", "email": "test@example.com"})
    assert created.status_code == 201
    new_id = created.json()["id"]
    deleted = client.delete(f"/users/{new_id}")
    assert deleted.status_code == 200
    assert deleted.json()["message"] == "User deleted"
    assert client.get(f"/users/{new_id}").status_code == 404


def test_delete_user_not_found():
    response = client.delete("/users/999")
    assert response.status_code == 404
