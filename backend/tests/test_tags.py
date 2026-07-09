from uuid import uuid4

from app.models import AuditLog

def test_create_tag(client_factory, db_session):
    client = client_factory()
    response = client.post(
        "/api/tags/",
        json={
            "name": "Test Tag",
            "description": "This is a test tag",
            "color": "#FF5733"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Test Tag"
    assert data["description"] == "This is a test tag"
    assert data["color"] == "#FF5733"
    assert "id" in data

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == data["id"]).all()
    assert len(audit_logs) == 1
    assert audit_logs[0].action == "create"
    assert audit_logs[0].entity_type == "tag"

def test_get_tags(client_factory):
    client = client_factory()
    response = client.get("/api/tags/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_tag(client_factory, db_session):
    client = client_factory()
    created = client.post(
        "/api/tags/",
        json={
            "name": "Update Tag",
            "description": "This tag will be updated",
            "color": "#33FF57"
        }
    )

    assert created.status_code == 200
    tag_id = created.json()["id"]

    response = client.put(
        f"/api/tags/{tag_id}",
        json={
            "name": "Updated Tag",
            "description": "This tag has been updated",
            "color": "#3357FF"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Updated Tag"
    assert data["description"] == "This tag has been updated"
    assert data["color"] == "#3357FF"

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == tag_id).order_by(AuditLog.created_at).all()
    assert len(audit_logs) == 2
    assert audit_logs[1].action == "update"
    assert audit_logs[1].entity_type == "tag"
    assert audit_logs[1].old_values["name"] == "Update Tag"
    assert audit_logs[1].new_values["name"] == "Updated Tag"
    assert audit_logs[1].old_values["color"] == "#33FF57"
    assert audit_logs[1].new_values["color"] == "#3357FF"

def test_delete_tag(client_factory, db_session):
    client = client_factory()
    created = client.post(
        "/api/tags/",
        json={
            "name": "Delete Tag",
            "description": "This tag will be deleted",
            "color": "#FF33A1"
        }
    )

    assert created.status_code == 200
    tag_id = created.json()["id"]

    response = client.delete(f"/api/tags/{tag_id}")

    assert response.status_code == 200
    assert response.json()["detail"] == "Tag deleted successfully"

    response = client.get("/api/tags/")
    deleted_tag = [t for t in response.json() if t["id"] == tag_id]
    assert len(deleted_tag) == 0

    ## Verify auditing
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == tag_id).order_by(AuditLog.created_at).all()
    assert len(audit_logs) == 2
    assert audit_logs[1].action == "delete"
    assert audit_logs[1].entity_type == "tag"
    assert audit_logs[1].old_values["name"] == "Delete Tag"