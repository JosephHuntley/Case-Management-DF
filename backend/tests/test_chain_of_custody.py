from app.models import EvidenceType, AcquisitionMethod, CustodyAction, AuditLog, AuditAction
from datetime import datetime, timezone
from uuid import UUID
from helper import create_test_case, create_test_user


def test_create_chain_of_custody(client_factory, db_session):
    client = client_factory()
    user = create_test_user(client)
    user2 = create_test_user(client)
    case = create_test_case(client)
    case_id = case.json()["id"]

    item = client.post("/api/evidence-items", json={
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
    response = client.post("/api/chain-of-custody/", json={
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
    user = create_test_user(client)
    case = create_test_case(client)
    case_id = case.json()["id"]

    item = client.post("/api/evidence-items", json={
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

    chain = client.post("/api/chain-of-custody/", json={
        "evidence_id": item.json()["id"],
        "from_person": user.json()["id"],
        "notes": "Initial collection of evidence",
        "action": CustodyAction.COLLECTED.value
    })

    response = client.get(f"/api/chain-of-custody/{chain.json()["id"]}")

    assert response.status_code == 200
    assert response.json()["evidence_id"] == item.json()["id"]
    assert response.json()["from_person"] == user.json()["id"]
    assert response.json()["to_person"] is None
    assert response.json()["notes"] == "Initial collection of evidence"
    assert response.json()["action"] == CustodyAction.COLLECTED.value

def test_get_chain_by_id(client_factory, db_session):
    client = client_factory()
    user = create_test_user(client)
    case = create_test_case(client)
    case_id = case.json()["id"]

    item = client.post("/api/evidence-items", json={
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

    chain = client.post("/api/chain-of-custody/", json={
        "evidence_id": item.json()["id"],
        "from_person": user.json()["id"],
        "notes": "Initial collection of evidence",
        "action": CustodyAction.COLLECTED.value
    })

    response = client.get(f"/api/chain-of-custody/evidence/{item.json()["id"]}")

    assert response.status_code == 200
    assert response.json()[0]["evidence_id"] == item.json()["id"]
    assert response.json()[0]["from_person"] == user.json()["id"]
    assert response.json()[0]["to_person"] is None
    assert response.json()[0]["notes"] == "Initial collection of evidence"
    assert response.json()[0]["action"] == CustodyAction.COLLECTED.value