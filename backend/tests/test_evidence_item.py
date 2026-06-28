from datetime import datetime, timezone
from app.models.evidence_item import EvidenceType, AcquisitionMethod
from app.models.audit_log import AuditLog, AuditAction
from uuid import UUID

def test_item_create(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "evidenceuser1",
        "email": "evidenceuser1@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Evidence",
        "description": "This case is for testing evidence items",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })

    case_id = case.json()["id"]
    evidence = client.post("/evidence-items/", json={
        "case_id": case_id,
        "acquired_by": user.json()["id"],
        "evidence_tag": "E-0001-P-ATL",
        "name": f"iPhone case# {case_id}",
        "description": "iPhone 7, serial number 11204930",
        "evidence_type": EvidenceType.DISK_IMAGE.value,
        "source_path": "C://test/Example/E-0001-P-ATL.001",
        "acquisition_method": AcquisitionMethod.CELLEBRITE.value,
        "acquired_at": datetime.now(timezone.utc).isoformat(),
        "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
        "md5": "65a8e27d8879283831b664bd8b7f0ad4",
        "size_bytes": 1000123,
        "is_verified": True
    })

    audit_logs = db_session.query(AuditLog).filter(
        AuditLog.entity_id == UUID(evidence.json()["id"])
    ).order_by(AuditLog.created_at).all()
    assert len(audit_logs) == 1
    assert audit_logs[0].action == "create"
    assert audit_logs[0].entity_type == "evidence_item"

    assert evidence.status_code == 200
    assert evidence.json()["evidence_tag"] == "E-0001-P-ATL"
    assert evidence.json()["acquired_by"] == user.json()["id"]
    assert evidence.json()["is_verified"] == True
    assert evidence.json()["case_id"] == case_id    
    assert evidence.json()["name"] == f"iPhone case# {case_id}"
    assert evidence.json()["description"] == "iPhone 7, serial number 11204930"
    assert evidence.json()["evidence_type"] == "disk_image"
    assert evidence.json()["source_path"] == "C://test/Example/E-0001-P-ATL.001"
    assert evidence.json()["acquisition_method"] == "cellebrite"
    assert evidence.json()["acquired_at"] is not None
    assert evidence.json()["sha256"] == "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    assert evidence.json()["md5"] == "65a8e27d8879283831b664bd8b7f0ad4"
    assert evidence.json()["size_bytes"] == 1000123

def test_get_by_id(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "evidenceuser2",
        "email": "evidenceuser2@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Evidence",
        "description": "This case is for testing evidence items",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })

    timestamp = datetime.now(timezone.utc).isoformat()

    case_id = case.json()["id"]
    evidence = client.post("/evidence-items/", json={
        "case_id": case_id,
        "acquired_by": user.json()["id"],
        "evidence_tag": "E-0001-P-ATL",
        "name": f"iPhone case# {case_id}",
        "description": "iPhone 7, serial number 11204930",
        "evidence_type": EvidenceType.DISK_IMAGE.value,
        "source_path": "C://test/Example/E-0001-P-ATL.001",
        "acquisition_method": AcquisitionMethod.CELLEBRITE.value,
        "acquired_at": timestamp,
        "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
        "md5": "65a8e27d8879283831b664bd8b7f0ad4",
        "size_bytes": 1000123,
        "is_verified": True
    })

    item_id = evidence.json()["id"]
    response = client.get(f"/evidence-items/{item_id}")

    assert response.json()["case_id"] == case_id
    assert response.json()["acquired_by"] == user.json()["id"]
    assert response.json()["evidence_tag"] == "E-0001-P-ATL"
    assert response.json()["name"] == f"iPhone case# {case_id}"
    assert response.json()["description"] == "iPhone 7, serial number 11204930"
    assert response.json()["evidence_type"] == EvidenceType.DISK_IMAGE.value
    assert response.json()["source_path"] == "C://test/Example/E-0001-P-ATL.001"
    assert response.json()["acquisition_method"] == AcquisitionMethod.CELLEBRITE.value
    assert response.json()["acquired_at"] is not None
    assert response.json()["sha256"] == "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    assert response.json()["md5"] == "65a8e27d8879283831b664bd8b7f0ad4"
    assert response.json()["size_bytes"] == 1000123
    assert response.json()["is_verified"] == True

def test_get_by_case_id(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "evidenceuser3",
        "email": "evidenceuser3@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Evidence",
        "description": "This case is for testing evidence items",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })

    timestamp = datetime.now(timezone.utc).isoformat()

    case_id = case.json()["id"]
    evidence = client.post("/evidence-items/", json={
        "case_id": case_id,
        "acquired_by": user.json()["id"],
        "evidence_tag": "E-0001-P-ATL",
        "name": f"iPhone case# {case_id}",
        "description": "iPhone 7, serial number 11204930",
        "evidence_type": EvidenceType.DISK_IMAGE.value,
        "source_path": "C://test/Example/E-0001-P-ATL.001",
        "acquisition_method": AcquisitionMethod.CELLEBRITE.value,
        "acquired_at": timestamp,
        "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
        "md5": "65a8e27d8879283831b664bd8b7f0ad4",
        "size_bytes": 1000123,
        "is_verified": True
    })

    item_id = evidence.json()["id"]
    response = client.get(f"/evidence-items/case/{case_id}")

    assert len(response.json()) == 1

def test_update_item(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "evidenceuser4",
        "email": "evidenceuser4@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Evidence",
        "description": "This case is for testing evidence items",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })

    timestamp = datetime.now(timezone.utc).isoformat()

    case_id = case.json()["id"]
    evidence = client.post("/evidence-items/", json={
        "case_id": case_id,
        "acquired_by": user.json()["id"],
        "evidence_tag": "E-0001-P-ATL",
        "name": f"iPhone case# {case_id}",
        "description": "iPhone 7, serial number 11204930",
        "evidence_type": EvidenceType.DISK_IMAGE.value,
        "source_path": "C://test/Example/E-0001-P-ATL.001",
        "acquisition_method": AcquisitionMethod.CELLEBRITE.value,
        "acquired_at": timestamp,
        "sha256": "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
        "md5": "65a8e27d8879283831b664bd8b7f0ad4",
        "size_bytes": 1000123,
        "is_verified": True
    })

    item_id = evidence.json()["id"]
    response = client.put(f"/evidence-items/{item_id}", json={
        "source_path": "D://test/Example/E-001-P-ATL.001"
    })

    assert response.status_code == 200
    body = response.json()
    assert body["source_path"] == "D://test/Example/E-001-P-ATL.001"
    assert body["name"] == f"iPhone case# {case_id}"
    assert body["description"] == "iPhone 7, serial number 11204930"
    assert body["md5"] == "65a8e27d8879283831b664bd8b7f0ad4"
    assert body["is_verified"] is True