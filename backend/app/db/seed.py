from uuid import uuid4, UUID
from app.db.session import SessionLocal
from app.models import User, UserRole, Case, CaseStatus, CasePriority, Tag, EvidenceItem, EvidenceType, AcquisitionMethod
from datetime import datetime, timezone
from app.security import hash_password


def seed_db():
    db = SessionLocal()

    if db.query(User).first():
        db.close()
        return

    admin = User(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        username="admin",
        email="admin@test.local",
        password_hash=hash_password("password"),
        role=UserRole.ADMIN,
        first_name="John",
        last_name="Doe"
    )
    investigator = User(
        id=uuid4(),
        username="investigator",
        email="investigator@test.local",
        password_hash=hash_password("diffPassword"),
        role=UserRole.INVESTIGATOR,
        first_name="Jane",
        last_name="Doe"
    )
    db.add_all([admin, investigator])

    malware_tag = Tag(
        id=uuid4(),
        name="malware",
        description="Cases involving malware",
        color="#FF0000"
    )
    windows_tag = Tag(
        id=uuid4(),
        name="windows",
        description="Cases involving Windows OS",
        color="#0078D7"
    )
    triage_tag = Tag(
        id=uuid4(),
        name="triage",
        description="Cases that need to be triaged",
        color="#FFA500"
    )
    db.add_all([malware_tag, windows_tag, triage_tag])

    case = Case(
        id=uuid4(),
        case_number="CASE-2026-0001",
        title="Test Forensic Case",
        description="Development seed data",
        status=CaseStatus.OPEN,
        priority=CasePriority.HIGH,
        created_by=investigator.id
    )
    case.tags.extend([malware_tag, windows_tag, triage_tag])
    db.add(case)

    item = EvidenceItem(
        id=uuid4(),
        case_id=case.id,
        acquired_by=admin.id,
        evidence_tag="E-0001-P-ATL",
        name=f"iPhone case# {case.id}",
        description="iPhone 7, serial number 11204930",
        evidence_type=EvidenceType.DISK_IMAGE.value,
        source_path="C://test/Example/E-0001-P-ATL.001",
        acquisition_method=AcquisitionMethod.CELLEBRITE.value,
        acquired_at=datetime.now(timezone.utc).isoformat(),
        sha256="dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f",
        md5="65a8e27d8879283831b664bd8b7f0ad4",
        size_bytes=1000123,
        is_verified=True
    )
    db.add(item)

    db.commit()
    db.close()