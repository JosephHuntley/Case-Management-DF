from uuid import uuid4


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["role"] == "investigator"
    assert "id" in data


def test_get_users(client):
    response = client.get("/users/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(client):
    created = client.post(
        "/users/",
        json={
            "username": "lookupuser",
            "email": "lookup@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert created.status_code == 200

    user_id = created.json()["id"]

    response = client.get(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["id"] == user_id


def test_get_missing_user(client):
    response = client.get(f"/users/{uuid4()}")

    assert response.status_code == 404


def test_update_user(client):
    created = client.post(
        "/users/",
        json={
            "username": "updateuser",
            "email": "update@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert created.status_code == 200

    user_id = created.json()["id"]

    response = client.put(
        f"/users/{user_id}",
        json={
            "role": "admin"
        }
    )

    assert response.status_code == 200
    assert response.json()["role"] == "admin"


def test_delete_user(client):
    created = client.post(
        "/users/",
        json={
            "username": "deleteuser",
            "email": "delete@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert created.status_code == 200

    user_id = created.json()["id"]

    response = client.delete(f"/users/{user_id}")

    assert response.status_code == 200
    assert response.json()["message"] == "user archived"