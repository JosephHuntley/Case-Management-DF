from uuid import UUID, uuid4

from app.models.audit_log import AuditLog


def test_create_case_note(client, db_session):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser1",
            "email": "caseuser1@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )

    case = client.post(
        "/cases/",
        json={
            "title": "Test Case for Notes",
            "description": "This case is for testing case notes",
            "status": "open",
            "priority": "medium",
            "created_by": user.json()["id"]
        }
    )   

    response = client.post(
        "/case-notes/",
        json={
            "case_id": case.json()["id"],
            "note": "This is a test case note"
        }    )
    
    assert response.status_code == 200
    assert response.json()["note"] == "This is a test case note"
    assert response.json()["author_id"] == "11111111-1111-1111-1111-111111111111"

    ## Verify it's audited
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == response.json()["id"]).order_by(AuditLog.created_at).all()
    assert audit_logs[-1].action == "create"
    assert audit_logs[-1].entity_type == "case_note"
    assert audit_logs[-1].changed_by == UUID("11111111-1111-1111-1111-111111111111")
    assert audit_logs[-1].new_values["note"] == "This is a test case note"

def test_get_case_note_by_id(client, db_session):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser4",
            "email": "caseuser4@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )
    case = client.post(
        "/cases/",
        json={
            "title": "Test Case for Note Retrieval",
            "description": "This case is for testing retrieval of case notes",
            "status": "open",
            "priority": "medium",
            "created_by": user.json()["id"]
        }
    )
    note_response = client.post(
        "/case-notes/",
        json={
            "case_id": case.json()["id"],
            "note": "This is a test case note for retrieval"
        }
    )   

    note_id = note_response.json()["id"]
    response = client.get(f"/case-notes/{note_id}")

    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["note"] == "This is a test case note for retrieval"
    assert response.json()["author_id"] == "11111111-1111-1111-1111-111111111111"

    def test_get_missing_case_note_by_id(client):
        response = client.get(f"/case-notes/{uuid4()}")
        assert response.status_code == 404
    
    def test_get_case_notes_by_case_id(client, db_session):
        user = client.post(
            "/users/",
            json={
                "username": "caseuser5",
                "email": "caseuser5@example.com",
                "password": "password123",
                "role": "investigator"
            }
        )
        case = client.post(
            "/cases/",
            json={
                "title": "Test Case for Notes List",
                "description": "This case is for testing retrieval of case notes list",
                "status": "open",
                "priority": "medium",
                "created_by": user.json()["id"]
            }
        )
        for i in range(3):
            client.post(
                "/case-notes/",
                json={
                    "case_id": case.json()["id"],
                    "note": f"This is test case note {i+1}"
                }
            )
        response = client.get(f"/case-notes/case/{case.json()['id']}")

        assert response.status_code == 200
        assert len(response.json()) == 3
        for i in range(3):
            assert response.json()[i]["note"] == f"This is test case note {i+1}"
            assert response.json()[i]["author_id"] == "11111111-1111-1111-1111-111111111111"

    def test_delete_case_note(client, db_session):
        user = client.post(
            "/users/",
            json={
                "username": "caseuser6",
                "email": "caseuser6@example.com",
                "password": "password123",
                "role": "investigator"
            }
        )
        case = client.post(
            "/cases/",
            json={
                "title": "Test Case for Note Deletion",
                "description": "This case is for testing deletion of case notes",
                "status": "open",
                "priority": "medium",
                "created_by": user.json()["id"]
            }
        )
        note_response = client.post(
            "/case-notes/",
            json={
                "case_id": case.json()["id"],
                "note": "This is a test case note for deletion"
            }
        )
        note_id = note_response.json()["id"]
        response = client.delete(f"/case-notes/{note_id}")

        assert response.status_code == 200
        assert response.json()["id"] == note_id
        assert response.json()["is_archived"] == True

        ## Verify it's audited 
        audit_response = client.get(f"/audit-logs/case-note/{note_id}")
        assert audit_response.status_code == 200
        audit_logs = audit_response.json()
        assert len(audit_logs) == 1
        assert audit_logs[0]["action"] == "delete"
        assert audit_logs[0]["entity_type"] == "case_note"

def test_update_case_note(client, db_session):
    user = client.post(
        "/users/",
        json={
            "username": "caseuser7",
            "email": "caseuser7@example.com",
            "password": "password123",
            "role": "investigator"
        }
    )
    case = client.post(
        "/cases/",
        json={
            "title": "Test Case for Note Update",
            "description": "This case is for testing update of case notes",
            "status": "open",
            "priority": "medium",
            "created_by": user.json()["id"]
        }
    )
    note_response = client.post(
        "/case-notes/",
        json={
            "case_id": case.json()["id"],
            "note": "This is a test case note for update"
        }
    )
    note_id = note_response.json()["id"]
    response = client.put(
        f"/case-notes/{note_id}",
        json={
            "note": "This is an updated test case note",
            "case_id": case.json()["id"]
        }
    )
    assert response.status_code == 200
    assert response.json()["id"] == note_id
    assert response.json()["note"] == "This is an updated test case note"
    assert response.json()["author_id"] == "11111111-1111-1111-1111-111111111111"

    ## Verify it's audited
    audit_logs = db_session.query(AuditLog).filter(AuditLog.entity_id == response.json()["id"]).order_by(AuditLog.created_at).all()
    assert audit_logs[-1].action == "update"
    assert audit_logs[-1].entity_type == "case_note"
    assert audit_logs[-1].changed_by == UUID("11111111-1111-1111-1111-111111111111")
    assert audit_logs[-1].old_values["note"] == "This is a test case note for update"
    assert audit_logs[-1].new_values["note"] == "This is an updated test case note"