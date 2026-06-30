from time import sleep
from uuid import UUID
from helper import create_test_user
from app.main import app
from app.security import get_current_user
from app.core.config import settings


def test_login(client_factory, db_session):
    client = client_factory()

    user = create_test_user(client)
    assert user.status_code == 201 

    response = client.post("/auth/login", data={  
        "grant_type": "password",
        "username": user.json()["username"],
        "password": "password123",
    })

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert body.get("token_type") == "bearer"

def test_login_invalid_user(client_factory, db_session):
    client = client_factory()

    user = create_test_user(client)
    assert user.status_code == 201

    response = client.post("/auth/login/", data={
        "grant_type": "password",
        "username": "invalidusername",
        "password": "password123",
    })

    assert response.status_code == 401

def test_login_invalid_password(client_factory, db_session):
    client = client_factory()

    user = create_test_user(client)
    assert user.status_code == 201

    response = client.post("/auth/login/", data={
        "grant_type": "password",
        "username": user.json()["username"],
        "password": "invalidpassword",
    })

    assert response.status_code == 401

def test_invalid_authorization(client_factory, db_session):
    client = client_factory(user_id=UUID("11111111-1111-1111-1111-111111111112"))
    
    user = create_test_user(client)
    assert user.status_code == 403

def test_refresh_token(client_factory):
    client = client_factory()

    user = create_test_user(client)
    assert user.status_code == 201

    login = client.post("/auth/login/", data={
        "grant_type": "password",
        "username": user.json()["username"],
        "password": "password123",
    })

    assert login.status_code == 200
    assert "refresh_token" in login.json()

    old_refresh = login.json()["refresh_token"]

    response = client.post("/auth/refresh", json={"refresh_token": old_refresh})
    assert response.status_code == 200
    assert response.json()["access_token"] != login.json()["access_token"]
    assert response.json()["refresh_token"] != old_refresh

    # Old refresh token should now be rejected
    reuse = client.post("/auth/refresh", json={"refresh_token": old_refresh})
    assert reuse.status_code == 401

def test_no_token_rejected(client_factory):
    client = client_factory()
    app.dependency_overrides.pop(get_current_user, None) 
    response = client.get("/users")
    assert response.status_code == 401

def test_malformed_token_rejected(client_factory):
    client = client_factory()
    app.dependency_overrides.pop(get_current_user, None)
    response = client.get("/users", headers={"Authorization": "Bearer not-a-real-token"})
    assert response.status_code == 401

def test_token_uniqueness(client_factory):
    # Likely a redundant test with rate limiter in place. However, this test was developed prior to the limiter and 
    # JTI was added to ensure JWT tokens remained unique even when they're created during the same second.
    settings.RATE_LIMIT_ENABLED = False
    client = client_factory()
    user = create_test_user(client, username="testuserunique")

    login1 = client.post("/auth/login", data={"grant_type": "password", "username": "testuserunique", "password": "password123"})
    login2 = client.post("/auth/login", data={"grant_type": "password", "username": "testuserunique", "password": "password123"})

    assert login1.json()["access_token"] != login2.json()["access_token"]

    settings.RATE_LIMIT_ENABLED = True

def test_limiter(client_factory):
    client = client_factory()

    user = create_test_user(client)

    client.post("/auth/login", data={"grant_type": "password", "username": user.json()["username"], "password": "password123"})
    response = client.post("/auth/login", data={"grant_type": "password", "username": user.json()["username"], "password": "password123"})

    assert response.status_code == 429