from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_register_success(test_user_data):
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_register_username_taken(test_user_data):
    response = client.post("/auth/register", json=test_user_data)
    response = client.post("/auth/register", json=test_user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Username taken"


def test_register_invalid_username():
    invalid_user = {
        "username": "invalid username",
        "password": "StrongPassword123!",
    }
    response = client.post("/auth/register", json=invalid_user)
    assert response.status_code == 422


def test_register_weak_password():
    invalid_user = {
        "username": "newuser",
        "password": "123",
    }
    response = client.post("/auth/register", json=invalid_user)
    assert response.status_code == 422


def test_login_success(test_user):
    response = client.post("/auth/token", data=test_user)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_credentials(test_user):
    form_data = {
        "username": test_user["username"],
        "password": "WrongPassword",
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_refresh_token_flow(test_user):
    response = client.post("/auth/token", data=test_user)
    tokens = response.json()
    refresh_token = tokens["refresh_token"]

    form_data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    response = client.post("/auth/token", data=form_data)
    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert new_tokens["refresh_token"] == refresh_token
