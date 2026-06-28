from app.models import EvidenceType, AcquisitionMethod, CustodyAction, AuditLog, AuditAction
from datetime import datetime, timezone
from uuid import UUID


def test_create_chain_of_custody(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "custodyuser1",
        "email": "custodyuser1@example.com",
        "password": "password123",
        "role": "investigator"
    })
    user2 = client.post("/users/", json={
        "username": "custodyuser1.5",
        "email": "custodyuser1_5@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Chain of Custody",
        "description": "This case is for testing creation of chain of custody records",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })
    case_id = case.json()["id"]

    item = client.post("/evidence-items", json={
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

    # This is a bad example as there should be no 'to_person' on a collected evidence. But I'm testing to ensure both fields keep their value
    response = client.post("/chain-of-custody/", json={
        "evidence_id": item.json()["id"],
        "from_person": user.json()["id"],
        "to_person": user2.json()["id"],
        "notes": "Initial collection of evidence",
        "action": CustodyAction.COLLECTED.value
    })

    assert response.status_code == 200
    assert response.json()["evidence_id"] == item.json()["id"]
    assert response.json()["from_person"] == user.json()["id"]
    assert response.json()["to_person"] == user2.json()["id"]
    assert response.json()["to_person"] != user.json()["id"]
    assert response.json()["notes"] == "Initial collection of evidence"
    assert response.json()["action"] == CustodyAction.COLLECTED.value

    audit_logs = db_session.query(AuditLog).filter(
        AuditLog.entity_id == UUID(response.json()["id"])
    ).order_by(AuditLog.created_at).all()
    assert len(audit_logs) == 1
    assert audit_logs[0].action == AuditAction.CREATE.value
    assert audit_logs[0].entity_type == "chain_of_custody"

def test_get_chain_by_id(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "custodyuser2",
        "email": "custodyuser2@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Chain of Custody",
        "description": "This case is for testing creation of chain of custody records",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })
    case_id = case.json()["id"]

    item = client.post("/evidence-items", json={
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

    chain = client.post("/chain-of-custody/", json={
        "evidence_id": item.json()["id"],
        "from_person": user.json()["id"],
        "notes": "Initial collection of evidence",
        "action": CustodyAction.COLLECTED.value
    })

    response = client.get(f"/chain-of-custody/{chain.json()["id"]}")

    assert response.status_code == 200
    assert response.json()["evidence_id"] == item.json()["id"]
    assert response.json()["from_person"] == user.json()["id"]
    assert response.json()["to_person"] is None
    assert response.json()["notes"] == "Initial collection of evidence"
    assert response.json()["action"] == CustodyAction.COLLECTED.value

def test_get_chain_by_id(client_factory, db_session):
    client = client_factory()
    user = client.post("/users/", json={
        "username": "custodyuser3",
        "email": "custodyuser3@example.com",
        "password": "password123",
        "role": "investigator"
    })
    case = client.post("/cases/", json={
        "title": "Test Case for Chain of Custody",
        "description": "This case is for testing creation of chain of custody records",
        "status": "open",
        "priority": "medium",
        "created_by": user.json()["id"]
    })
    case_id = case.json()["id"]

    item = client.post("/evidence-items", json={
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

    chain = client.post("/chain-of-custody/", json={
        "evidence_id": item.json()["id"],
        "from_person": user.json()["id"],
        "notes": "Initial collection of evidence",
        "action": CustodyAction.COLLECTED.value
    })

    response = client.get(f"/chain-of-custody/evidence/{item.json()["id"]}")

    assert response.status_code == 200
    assert response.json()["evidence_id"] == item.json()["id"]
    assert response.json()["from_person"] == user.json()["id"]
    assert response.json()["to_person"] is None
    assert response.json()["notes"] == "Initial collection of evidence"
    assert response.json()["action"] == CustodyAction.COLLECTED.value