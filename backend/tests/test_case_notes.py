# test_case_notes.py
from uuid import UUID, uuid4
from app.models import AuditLog, AuditAction, UserRole
from helper import create_test_user, create_test_case


def test_create_case_note(client_factory, db_session):
    client = client_factory()
    
    case = create_test_case(client)

    response = client.post("/api/case-notes/", json={
        "case_id": case.json()["id"],
        "note": "This is a test case note"
    })

    assert response.status_code == 200
    assert response.json()["note"] == "This is a test case note"
    assert response.json()["author_id"] == "11111111-1111-1111-1111-111111111111"

    audit_logs = db_session.query(AuditLog).filter(
        AuditLog.entity_id == UUID(response.json()["id"])
    ).order_by(AuditLog.created_at).all()
    assert audit_logs[-1].action == AuditAction.CREATE
    assert audit_logs[-1].entity_type == "case_note"
    assert audit_logs[-1].changed_by == UUID("11111111-1111-1111-1111-111111111111")
    assert audit_logs[-1].new_values["note"] == "This is a test case note"


def test_get_case_note_by_id(client_factory, db_session):
    client = client_factory()
    
    case = create_test_case(client)

    note_response = client.post("/api/case-notes/", json={
        "case_id": case.json()["id"],
        "note": "This is a test case note for retrieval"
    })

    note_id = note_response.json()["id"]
    response = client.get(f"/api/case-notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["note"] == "This is a test case note for retrieval"
    assert response.json()["author_id"] == "11111111-1111-1111-1111-111111111111"


def test_get_missing_case_note_by_id(client_factory):
    client = client_factory()
    response = client.get(f"/api/case-notes/{uuid4()}")
    assert response.status_code == 404


def test_get_case_notes_by_case_id(client_factory, db_session):
    client = client_factory()
    case = create_test_case(client)

    for i in range(3):
        client.post("/api/case-notes/", json={
            "case_id": case.json()["id"],
            "note": f"This is test case note {i + 1}"
        })

    response = client.get(f"/api/case-notes/case/{case.json()['id']}")

    assert response.status_code == 200
    assert len(response.json()) == 3
    for i in range(3):
        assert response.json()[i]["note"] == f"This is test case note {i + 1}"
        assert response.json()[i]["author_id"] == "11111111-1111-1111-1111-111111111111"


def test_archive_case_note(client_factory, db_session):
    client = client_factory()
    case = create_test_case(client)

    note_response = client.post("/api/case-notes/", json={
        "case_id": case.json()["id"],
        "note": "This is a test case note for deletion"
    })

    note_id = note_response.json()["id"]
    response = client.delete(f"/api/case-notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["is_archived"] == True

    audit_logs = db_session.query(AuditLog).filter(
    AuditLog.entity_id == UUID(response.json()["id"])
).order_by(AuditLog.created_at).all()

    assert len(audit_logs) == 2
    assert audit_logs[-1].action == AuditAction.DELETE
    assert audit_logs[-1].entity_type == "case_note"


def test_update_case_note(client_factory, db_session):
    client = client_factory()
    case = create_test_case(client)

    note_response = client.post("/api/case-notes/", json={
        "case_id": case.json()["id"],
        "note": "This is a test case note for update"
    })

    note_id = note_response.json()["id"]
    response = client.put(f"/api/case-notes/{note_id}", json={
        "note": "This is an updated test case note",
        "case_id": case.json()["id"]
    })

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["note"] == "This is an updated test case note"
    assert response.json()["author_id"] == "11111111-1111-1111-1111-111111111111"

    audit_logs = db_session.query(AuditLog).filter(
        AuditLog.entity_id == UUID(response.json()["id"])
    ).order_by(AuditLog.created_at).all()
    assert audit_logs[-1].action == AuditAction.UPDATE
    assert audit_logs[-1].entity_type == "case_note"
    assert audit_logs[-1].changed_by == UUID("11111111-1111-1111-1111-111111111111")
    assert audit_logs[-1].old_values["note"] == "This is a test case note for update"
    assert audit_logs[-1].new_values["note"] == "This is an updated test case note"