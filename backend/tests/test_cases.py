from uuid import uuid4

from app.models import AuditLog

def test_create_case(client_factory, db_session):
    client = client_factory()
    user = client.post(
        "/users/",
        json={
            "username": "caseuser123",
            "email": "caseuser@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    tag = client.post(
        "/tags/",
        json={
            "name": "Test Tag1",
            "description": "This is a test tag",
            "color": "#FF0000"
        }
    )

    assert tag.status_code == 200
    tag_id = tag.json()["id"]

    response = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id,
            "tag_ids": []
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Test Case"
    assert data["description"] == "This is a test case"
    assert data["status"] == "open"
    assert data["priority"] == "medium"
    assert "id" in data

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == data["id"]).all()
    assert len(audit_logs) == 1
    assert audit_logs[0].action == "create"
    assert audit_logs[0].entity_type == "case"
    
def test_get_cases(client_factory):
    client = client_factory()
    response = client.get("/cases/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_case(client_factory):
    client = client_factory()
    user = client.post(
        "/users/",
        json={
            "username": "caseuser2",
            "email": "caseuser2@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    created = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert created.status_code == 200
    case_id = created.json()["id"]

    response = client.get(f"/cases/{case_id}")
    assert response.status_code == 200
    assert response.json()["id"] == case_id

def test_get_missing_cases(client_factory):
    client = client_factory()
    response = client.get(f"/cases/{uuid4()}")

    assert response.status_code == 404

def test_update_case(client_factory, db_session):
    client = client_factory()
    user = client.post(
        "/users/",
        json={
            "username": "caseuser3",
            "email": "caseuser3@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    created = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert created.status_code == 200
    case_id = created.json()["id"]

    response = client.put(
        f"/cases/{case_id}",
        json={
            "title": "Updated Test Case",
            "description": "This is an updated test case",
            "status": "in progress",
            "priority": "high"
        }
    )

    assert response.status_code == 200
    assert response.json()["id"] == case_id
    assert response.json()["title"] == "Updated Test Case"
    assert response.json()["description"] == "This is an updated test case"
    assert response.json()["status"] == "in progress"
    assert response.json()["priority"] == "high"

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == case_id).order_by(AuditLog.created_at).all()
    assert len(audit_logs) == 2
    assert audit_logs[1].action == "update"
    assert audit_logs[1].entity_type == "case"
    assert audit_logs[1].old_values["title"] == "Test Case"
    assert audit_logs[1].new_values["title"] == "Updated Test Case"
    assert audit_logs[1].old_values["status"] == "open"
    assert audit_logs[1].new_values["status"] == "in progress"

def test_delete_case(client_factory, db_session):
    client = client_factory()
    user = client.post(
        "/users/",
        json={
            "username": "caseuser42",
            "email": "caseuser24@test.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    assert user.status_code == 200
    user_id = user.json()["id"]

    created = client.post(
        "/cases/",
        json={
            "title": "Test Case",
            "description": "This is a test case",
            "status": "open",
            "priority": "medium",
            "created_by": user_id
        }
    )

    assert created.status_code == 200
    case_id = created.json()["id"]

    response = client.delete(f"/cases/{case_id}")
    assert response.status_code == 200

    get_all = client.get("/cases/")
    case_ids = [c["id"] for c in get_all.json()]
    assert case_id not in case_ids

    # Since it's a soft delete, we should still be able to get the case by ID, but it should be marked as deleted. 
    response = client.get(f"/cases/{case_id}")
    assert response.status_code == 200
    assert response.json()["deleted_at"] is not None

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == case_id).order_by(AuditLog.created_at).all()
    assert len(audit_logs) == 2
    assert audit_logs[1].action == "delete"
    assert audit_logs[1].entity_type == "case"
    assert audit_logs[1].old_values["title"] == "Test Case"
    assert audit_logs[1].new_values == None

