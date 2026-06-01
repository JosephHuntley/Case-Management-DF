from uuid import uuid4

from app.models.audit_log import AuditLog

def test_create_user(client, db_session):
    response = client.post(
        "/users/",
        json={
            "username": "testuser6748",
            "email": "test@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["username"] == "testuser6748"
    assert data["email"] == "test@example.com"
    assert data["role"] == "investigator"
    assert "id" in data

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == data["id"]).all()
    assert len(audit_logs) == 1
    assert audit_logs[0].action == "insert"
    assert audit_logs[0].entity_type == "User"


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


def test_update_user(client, db_session):
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

    data = response.json()
    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == data["id"]).all()
    assert len(audit_logs) == 2
    assert audit_logs[0].action == "insert"
    assert audit_logs[0].entity_type == "User"
    assert audit_logs[1].action == "update"
    assert audit_logs[1].new_values["role"] == "admin"
    assert audit_logs[1].old_values["role"] == "investigator"




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
    
    user_response = client.get(f"/users/{user_id}")
    assert user_response.json()["is_active"] == False
    assert user_response.json()["deleted_at"] is not None
