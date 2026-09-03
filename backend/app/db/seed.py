import hashlib
import json
from uuid import uuid4, UUID
from datetime import datetime, timedelta, timezone

from app.db.session import SessionLocal
from app.models import (
    User, UserRole,
    Case, CaseStatus, CasePriority,
    Tag,
    EvidenceItem, EvidenceType, AcquisitionMethod,
    ChainOfCustody, CustodyAction,
    CaseNote,
)
from app.security import hash_password


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def fake_sha256(seed: str) -> str:
    """Deterministic, plausible-looking sha256 hex digest for demo evidence."""
    return hashlib.sha256(seed.encode()).hexdigest()


def fake_md5(seed: str) -> str:
    return hashlib.md5(seed.encode()).hexdigest()


def compute_row_hash(evidence_id, performed_by, action, from_person, to_person, notes, previous_hash) -> str:
    """
    Mirrors ChainOfCustodyRepository._compute_row_hash exactly, so seeded
    chains pass verify_chain_of_custody() rather than relying on a
    placeholder/static hash.
    """
    action_value = action.value if hasattr(action, "value") else action
    payload = {
        "evidence_id": str(evidence_id),
        "performed_by": str(performed_by),
        "action": action_value,
        "from_person": str(from_person) if from_person else None,
        "to_person": str(to_person) if to_person else None,
        "notes": notes,
        "previous_hash": previous_hash,
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()


def add_custody_chain(db, evidence: EvidenceItem, events: list[dict]):
    """
    events: ordered list of dicts with keys:
        performed_by, action, from_person, to_person, notes, when (datetime)
    Builds a real linked hash chain, one entry per event.
    """
    previous_hash = None
    for ev in events:
        entry = ChainOfCustody(
            id=uuid4(),
            evidence_id=evidence.id,
            performed_by=ev["performed_by"],
            action=ev["action"],
            from_person=ev.get("from_person"),
            to_person=ev.get("to_person"),
            notes=ev.get("notes"),
            previous_hash=previous_hash,
        )
        entry.row_hash = compute_row_hash(
            entry.evidence_id, entry.performed_by, entry.action,
            entry.from_person, entry.to_person, entry.notes, previous_hash,
        )
        entry.created_at = ev["when"]
        db.add(entry)
        previous_hash = entry.row_hash


def days_ago(n, hour=9, minute=0):
    return (datetime.now(timezone.utc) - timedelta(days=n)).replace(
        hour=hour, minute=minute, second=0, microsecond=0
    )


# ---------------------------------------------------------------------------
# Seed
# ---------------------------------------------------------------------------

def seed_db():
    db = SessionLocal()

    if db.query(User).first():
        db.close()
        return

    # -----------------------------------------------------------------
    # Users
    # -----------------------------------------------------------------
    admin = User(
        id=UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        username="admin",
        email="admin@test.local",
        password_hash=hash_password("password"),
        role=UserRole.ADMIN,
        first_name="John",
        last_name="Doe",
    )
    m_reyes = User(
        id=uuid4(),
        username="m.reyes",
        email="m.reyes@test.local",
        password_hash=hash_password("diffPassword"),
        role=UserRole.INVESTIGATOR,
        first_name="Marcus",
        last_name="Reyes",
    )
    s_okafor = User(
        id=uuid4(),
        username="s.okafor",
        email="s.okafor@test.local",
        password_hash=hash_password("diffPassword"),
        role=UserRole.INVESTIGATOR,
        first_name="Sarah",
        last_name="Okafor",
    )
    d_lindqvist = User(
        id=uuid4(),
        username="d.lindqvist",
        email="d.lindqvist@test.local",
        password_hash=hash_password("diffPassword"),
        role=UserRole.INVESTIGATOR,
        first_name="David",
        last_name="Lindqvist",
    )
    r_park = User(
        id=uuid4(),
        username="r.park",
        email="r.park@test.local",
        password_hash=hash_password("diffPassword"),
        role=UserRole.AUDITOR,
        first_name="Regina",
        last_name="Park",
    )
    db.add_all([admin, m_reyes, s_okafor, d_lindqvist, r_park])
    db.flush()

    # -----------------------------------------------------------------
    # Tags
    # -----------------------------------------------------------------
    tag_malware = Tag(id=uuid4(), name="malware", description="Cases involving malware", color="#DC2626")
    tag_windows = Tag(id=uuid4(), name="windows", description="Windows OS artifacts", color="#0078D7")
    tag_macos = Tag(id=uuid4(), name="macos", description="macOS artifacts", color="#7C3AED")
    tag_mobile = Tag(id=uuid4(), name="mobile", description="Mobile device extraction", color="#059669")
    tag_insider = Tag(id=uuid4(), name="insider-threat", description="Suspected insider activity", color="#B45309")
    tag_ransomware = Tag(id=uuid4(), name="ransomware", description="Ransomware incident", color="#991B1B")
    tag_network = Tag(id=uuid4(), name="network-intrusion", description="External network intrusion", color="#1D4ED8")
    tag_ediscovery = Tag(id=uuid4(), name="ediscovery", description="Civil/HR e-discovery matter", color="#4B5563")
    tag_triage = Tag(id=uuid4(), name="triage", description="Needs initial triage", color="#EA580C")
    tag_legal_hold = Tag(id=uuid4(), name="legal-hold", description="Under active legal hold", color="#065F46")
    db.add_all([
        tag_malware, tag_windows, tag_macos, tag_mobile, tag_insider,
        tag_ransomware, tag_network, tag_ediscovery, tag_triage, tag_legal_hold,
    ])
    db.flush()

    # -----------------------------------------------------------------
    # Case 1 — Workstation exfiltration (open, in progress)
    # -----------------------------------------------------------------
    case1 = Case(
        id=uuid4(),
        case_number="CASE-2026-0001",
        title="Workstation Exfiltration — Finance Dept",
        description=(
            "Endpoint DLP flagged large outbound transfers from a finance analyst's "
            "workstation (FIN-WKS-0447) to a personal cloud storage account over a "
            "72-hour period prior to the employee's resignation. Scope includes disk "
            "imaging of the workstation and review of browser/cloud-sync artifacts."
        ),
        status=CaseStatus.IN_PROGRESS,
        priority=CasePriority.HIGH,
        created_by=m_reyes.id,
        assigned_to=m_reyes.id,
        opened_at=days_ago(21, 8, 30),
    )
    case1.tags.extend([tag_windows, tag_insider, tag_triage])
    db.add(case1)

    ev1a = EvidenceItem(
        id=uuid4(),
        case_id=case1.id,
        acquired_by=m_reyes.id,
        evidence_tag="E-2026-0001-01",
        name="FIN-WKS-0447 — Full Disk Image",
        description="512GB NVMe SSD, Dell Latitude 5540, imaged in place after custody transfer from IT Asset Management.",
        evidence_type=EvidenceType.DISK_IMAGE.value,
        source_path="\\\\forensics-nas\\cases\\2026-0001\\FIN-WKS-0447.E01",
        acquisition_method=AcquisitionMethod.FTK.value,
        acquired_at=days_ago(20, 10, 15).isoformat(),
        sha256=fake_sha256("case1-fin-wks-0447-image"),
        md5=fake_md5("case1-fin-wks-0447-image"),
        size_bytes=512_110_190_592,
        is_verified=True,
    )
    ev1b = EvidenceItem(
        id=uuid4(),
        case_id=case1.id,
        acquired_by=m_reyes.id,
        evidence_tag="E-2026-0001-02",
        name="FIN-WKS-0447 — Volatile Memory Capture",
        description="16GB RAM captured live prior to shutdown via WinPMEM before the workstation left the finance floor.",
        evidence_type=EvidenceType.MEMORY_DUMP.value,
        source_path="\\\\forensics-nas\\cases\\2026-0001\\FIN-WKS-0447.mem",
        acquisition_method=AcquisitionMethod.DD.value,
        acquired_at=days_ago(20, 10, 5).isoformat(),
        sha256=fake_sha256("case1-fin-wks-0447-mem"),
        md5=fake_md5("case1-fin-wks-0447-mem"),
        size_bytes=17_179_869_184,
        is_verified=True,
    )
    db.add_all([ev1a, ev1b])
    db.flush()

    add_custody_chain(db, ev1a, [
        dict(performed_by=m_reyes.id, action=CustodyAction.COLLECTED, to_person=m_reyes.id,
             notes="Disk imaged on-site with FTK Imager; write-blocker confirmed active.",
             when=days_ago(20, 10, 20)),
        dict(performed_by=m_reyes.id, action=CustodyAction.TRANSFERRED, from_person=m_reyes.id, to_person=s_okafor.id,
             notes="Handed off for parallel timeline analysis while memory capture is processed.",
             when=days_ago(17, 14, 0)),
        dict(performed_by=s_okafor.id, action=CustodyAction.CHECKED_OUT, from_person=s_okafor.id, to_person=s_okafor.id,
             notes="Checked out to forensic workstation FW-03 for Axiom processing.",
             when=days_ago(15, 9, 45)),
    ])
    add_custody_chain(db, ev1b, [
        dict(performed_by=m_reyes.id, action=CustodyAction.COLLECTED, to_person=m_reyes.id,
             notes="Live memory capture prior to shutdown to preserve volatile artifacts.",
             when=days_ago(20, 10, 10)),
    ])

    note1 = CaseNote(
        id=uuid4(), case_id=case1.id, author_id=m_reyes.id,
        note=(
            "Initial browser history review shows repeated access to a personal Google Drive "
            "account starting three days before the DLP alert. Cross-referencing with badge "
            "access logs to confirm on-site presence during transfer windows."
        ),
        created_at=days_ago(16, 11, 0),
    )
    note1b = CaseNote(
        id=uuid4(), case_id=case1.id, author_id=s_okafor.id,
        note="Axiom scan complete on the disk image. Flagged 340 files matching finance report naming conventions in the local sync folder for the personal cloud account.",
        created_at=days_ago(10, 13, 20),
    )
    db.add_all([note1, note1b])

    # -----------------------------------------------------------------
    # Case 2 — Mobile extraction, HR complaint (closed)
    # -----------------------------------------------------------------
    case2 = Case(
        id=uuid4(),
        case_number="CASE-2026-0002",
        title="Mobile Device Extraction — HR Complaint",
        description=(
            "HR referral following a harassment complaint. Employee-owned iPhone provided "
            "voluntarily under a signed consent form for extraction of relevant SMS/iMessage "
            "and app-based messaging content within a defined date range."
        ),
        status=CaseStatus.CLOSED,
        priority=CasePriority.MEDIUM,
        created_by=s_okafor.id,
        assigned_to=s_okafor.id,
        opened_at=days_ago(64, 9, 0),
        closed_at=days_ago(38, 16, 30),
    )
    case2.tags.extend([tag_mobile, tag_ediscovery, tag_legal_hold])
    db.add(case2)

    ev2a = EvidenceItem(
        id=uuid4(),
        case_id=case2.id,
        acquired_by=s_okafor.id,
        evidence_tag="E-2026-0002-01",
        name="iPhone 13 — Logical Extraction",
        description="iPhone 13, 128GB, serial C7Q1F2XKQP. Consent-based logical extraction limited to messaging and call log data.",
        evidence_type=EvidenceType.OTHER.value,  # no MOBILE_DEVICE type in current enum
        source_path="\\\\forensics-nas\\cases\\2026-0002\\iphone13-logical.zip",
        acquisition_method=AcquisitionMethod.CELLEBRITE.value,
        acquired_at=days_ago(63, 11, 0).isoformat(),
        sha256=fake_sha256("case2-iphone13-logical"),
        md5=fake_md5("case2-iphone13-logical"),
        size_bytes=1_884_312_064,
        is_verified=True,
    )
    db.add(ev2a)
    db.flush()

    add_custody_chain(db, ev2a, [
        dict(performed_by=s_okafor.id, action=CustodyAction.COLLECTED, to_person=s_okafor.id,
             notes="Extraction performed with device owner present per signed consent form (on file, HR-2026-014).",
             when=days_ago(63, 11, 20)),
        dict(performed_by=s_okafor.id, action=CustodyAction.TRANSFERRED, from_person=s_okafor.id, to_person=r_park.id,
             notes="Transferred to auditor for review prior to HR report finalization.",
             when=days_ago(45, 10, 0)),
        dict(performed_by=r_park.id, action=CustodyAction.RETURNED, from_person=r_park.id, to_person=s_okafor.id,
             notes="Review complete, no discrepancies noted. Returned to case owner for closure.",
             when=days_ago(40, 15, 0)),
        dict(performed_by=s_okafor.id, action=CustodyAction.ARCHIVED, from_person=s_okafor.id, to_person=s_okafor.id,
             notes="Case closed; extraction archived per retention policy.",
             when=days_ago(38, 16, 30)),
    ])

    note2 = CaseNote(
        id=uuid4(), case_id=case2.id, author_id=s_okafor.id,
        note="Findings summarized in Report R-2026-0002. Relevant message threads corroborate the complainant's timeline. No further extraction required.",
        is_archived=True,
        created_at=days_ago(39, 9, 0),
    )
    db.add(note2)

    # -----------------------------------------------------------------
    # Case 3 — Server compromise, external IP (open)
    # -----------------------------------------------------------------
    case3 = Case(
        id=uuid4(),
        case_number="CASE-2026-0003",
        title="Server Compromise — External IP",
        description=(
            "SIEM correlation alert for anomalous outbound connections from the "
            "customer-facing web server (WEB-PROD-02) to an external IP associated "
            "with known C2 infrastructure. Investigating for lateral movement and "
            "potential data staging prior to containment."
        ),
        status=CaseStatus.OPEN,
        priority=CasePriority.CRITICAL,
        created_by=d_lindqvist.id,
        assigned_to=d_lindqvist.id,
        opened_at=days_ago(4, 6, 45),
    )
    case3.tags.extend([tag_network, tag_windows, tag_ransomware])
    db.add(case3)

    ev3a = EvidenceItem(
        id=uuid4(),
        case_id=case3.id,
        acquired_by=d_lindqvist.id,
        evidence_tag="E-2026-0003-01",
        name="WEB-PROD-02 — Memory Capture",
        description="Live memory acquisition performed remotely via out-of-band management interface prior to isolation.",
        evidence_type=EvidenceType.MEMORY_DUMP.value,
        source_path="\\\\forensics-nas\\cases\\2026-0003\\web-prod-02.mem",
        acquisition_method=AcquisitionMethod.DD.value,
        acquired_at=days_ago(4, 7, 10).isoformat(),
        sha256=fake_sha256("case3-webprod02-mem"),
        md5=fake_md5("case3-webprod02-mem"),
        size_bytes=34_359_738_368,
        is_verified=True,
    )
    ev3b = EvidenceItem(
        id=uuid4(),
        case_id=case3.id,
        acquired_by=d_lindqvist.id,
        evidence_tag="E-2026-0003-02",
        name="Perimeter Firewall — 72hr PCAP",
        description="Full packet capture from perimeter firewall spanning the 72 hours prior to and including the alert window.",
        evidence_type=EvidenceType.NETWORK_CAPTURE.value,
        source_path="\\\\forensics-nas\\cases\\2026-0003\\perimeter-72hr.pcap",
        acquisition_method=AcquisitionMethod.OTHER.value,
        acquired_at=days_ago(4, 8, 0).isoformat(),
        sha256=fake_sha256("case3-perimeter-pcap"),
        md5=fake_md5("case3-perimeter-pcap"),
        size_bytes=9_663_676_416,
        is_verified=False,
    )
    ev3c = EvidenceItem(
        id=uuid4(),
        case_id=case3.id,
        acquired_by=d_lindqvist.id,
        evidence_tag="E-2026-0003-03",
        name="WEB-PROD-02 — Application & Auth Logs",
        description="Exported application, IIS, and Windows Security event logs covering the 14 days prior to detection.",
        evidence_type=EvidenceType.LOG_FILE.value,
        source_path="\\\\forensics-nas\\cases\\2026-0003\\web-prod-02-logs.zip",
        acquisition_method=AcquisitionMethod.MANUAL.value,
        acquired_at=days_ago(3, 13, 30).isoformat(),
        sha256=fake_sha256("case3-webprod02-logs"),
        md5=fake_md5("case3-webprod02-logs"),
        size_bytes=1_207_959_552,
        is_verified=True,
    )
    db.add_all([ev3a, ev3b, ev3c])
    db.flush()

    add_custody_chain(db, ev3a, [
        dict(performed_by=d_lindqvist.id, action=CustodyAction.COLLECTED, to_person=d_lindqvist.id,
             notes="Captured remotely under incident bridge authorization; hash verified immediately post-capture.",
             when=days_ago(4, 7, 15)),
    ])
    add_custody_chain(db, ev3b, [
        dict(performed_by=d_lindqvist.id, action=CustodyAction.COLLECTED, to_person=d_lindqvist.id,
             notes="Pulled from firewall retention buffer before rollover.",
             when=days_ago(4, 8, 5)),
        dict(performed_by=d_lindqvist.id, action=CustodyAction.TRANSFERRED, from_person=d_lindqvist.id, to_person=admin.id,
             notes="Shared with admin for cross-check against known IOC feed.",
             when=days_ago(3, 9, 0)),
    ])
    add_custody_chain(db, ev3c, [
        dict(performed_by=d_lindqvist.id, action=CustodyAction.COLLECTED, to_person=d_lindqvist.id,
             notes="Exported via native log export tooling; original logs left in place on source system.",
             when=days_ago(3, 13, 45)),
    ])

    note3a = CaseNote(
        id=uuid4(), case_id=case3.id, author_id=d_lindqvist.id,
        note="Outbound C2 IP resolves to infrastructure previously associated with a known ransomware affiliate. Escalating priority and looping in admin for IOC cross-check.",
        created_at=days_ago(4, 9, 0),
    )
    note3b = CaseNote(
        id=uuid4(), case_id=case3.id, author_id=admin.id,
        note="Confirmed IP overlap with three IOCs from last month's threat intel bulletin. Recommend isolating WEB-PROD-02 from the segment pending full triage.",
        created_at=days_ago(3, 10, 15),
    )
    db.add_all([note3a, note3b])

    # -----------------------------------------------------------------
    # Case 4 — Ransomware incident (in progress, critical)
    # -----------------------------------------------------------------
    case4 = Case(
        id=uuid4(),
        case_number="CASE-2026-0004",
        title="Ransomware Encryption Event — File Server Cluster",
        description=(
            "Overnight batch job failures led to discovery of encrypted shares across "
            "the primary file server cluster (FS-01/FS-02). Ransom note consistent with "
            "a known affiliate group. Investigation covers initial access vector, "
            "lateral movement, and backup integrity assessment."
        ),
        status=CaseStatus.IN_PROGRESS,
        priority=CasePriority.CRITICAL,
        created_by=d_lindqvist.id,
        assigned_to=m_reyes.id,
        opened_at=days_ago(9, 5, 20),
    )
    case4.tags.extend([tag_ransomware, tag_windows, tag_network])
    db.add(case4)

    ev4a = EvidenceItem(
        id=uuid4(),
        case_id=case4.id,
        acquired_by=m_reyes.id,
        evidence_tag="E-2026-0004-01",
        name="FS-01 — Targeted Disk Image (System Volume)",
        description="System volume imaged from FS-01 to preserve scheduled task artifacts and encryptor binary remnants prior to rebuild.",
        evidence_type=EvidenceType.DISK_IMAGE.value,
        source_path="\\\\forensics-nas\\cases\\2026-0004\\FS-01-C.E01",
        acquisition_method=AcquisitionMethod.FTK.value,
        acquired_at=days_ago(9, 8, 0).isoformat(),
        sha256=fake_sha256("case4-fs01-c-image"),
        md5=fake_md5("case4-fs01-c-image"),
        size_bytes=274_877_906_944,
        is_verified=True,
    )
    ev4b = EvidenceItem(
        id=uuid4(),
        case_id=case4.id,
        acquired_by=m_reyes.id,
        evidence_tag="E-2026-0004-02",
        name="Ransom Note (ReadMe_Recover.txt) — 6 copies",
        description="Ransom note text files recovered from six distinct directories across FS-01 and FS-02, preserved with original timestamps.",
        evidence_type=EvidenceType.DOCUMENT.value,
        source_path="\\\\forensics-nas\\cases\\2026-0004\\ransom-notes\\",
        acquisition_method=AcquisitionMethod.MANUAL.value,
        acquired_at=days_ago(9, 7, 30).isoformat(),
        sha256=fake_sha256("case4-ransom-notes"),
        md5=fake_md5("case4-ransom-notes"),
        size_bytes=18_432,
        is_verified=True,
    )
    db.add_all([ev4a, ev4b])
    db.flush()

    add_custody_chain(db, ev4a, [
        dict(performed_by=m_reyes.id, action=CustodyAction.COLLECTED, to_person=m_reyes.id,
             notes="Imaged prior to cluster rebuild; coordinated with infrastructure team for isolation window.",
             when=days_ago(9, 8, 20)),
        dict(performed_by=m_reyes.id, action=CustodyAction.TRANSFERRED, from_person=m_reyes.id, to_person=d_lindqvist.id,
             notes="Handed to network lead for correlation with perimeter alert timeline.",
             when=days_ago(7, 10, 0)),
    ])
    add_custody_chain(db, ev4b, [
        dict(performed_by=m_reyes.id, action=CustodyAction.COLLECTED, to_person=m_reyes.id,
             notes="Copied with native timestamps preserved via robocopy /B before any remediation touched the shares.",
             when=days_ago(9, 7, 40)),
    ])

    note4 = CaseNote(
        id=uuid4(), case_id=case4.id, author_id=m_reyes.id,
        note="Encryptor binary naming and note format match a known affiliate's toolkit from last quarter's threat intel. Backup snapshots from the prior 48 hours appear intact and unaffected.",
        created_at=days_ago(8, 12, 0),
    )
    db.add(note4)

    # -----------------------------------------------------------------
    # Case 5 — Departing employee IP theft (pending review)
    # -----------------------------------------------------------------
    case5 = Case(
        id=uuid4(),
        case_number="CASE-2026-0005",
        title="Departing Engineer — Source Code Repository Access Review",
        description=(
            "Legal requested a review of repository and file-share access logs for a "
            "senior engineer who resigned with two weeks' notice, following reports "
            "that the individual accepted a position with a direct competitor."
        ),
        status=CaseStatus.PENDING,
        priority=CasePriority.MEDIUM,
        created_by=s_okafor.id,
        opened_at=days_ago(2, 14, 0),
    )
    case5.tags.extend([tag_insider, tag_ediscovery, tag_triage])
    db.add(case5)

    ev5a = EvidenceItem(
        id=uuid4(),
        case_id=case5.id,
        acquired_by=s_okafor.id,
        evidence_tag="E-2026-0005-01",
        name="Git Repository Access & Clone Logs — Q3",
        description="Exported audit logs from the internal Git hosting platform covering repository access, clones, and large downloads for the engineer's account.",
        evidence_type=EvidenceType.LOG_FILE.value,
        source_path="\\\\forensics-nas\\cases\\2026-0005\\git-audit-q3.json",
        acquisition_method=AcquisitionMethod.MANUAL.value,
        acquired_at=days_ago(2, 15, 0).isoformat(),
        sha256=fake_sha256("case5-git-audit"),
        md5=fake_md5("case5-git-audit"),
        size_bytes=2_411_724,
        is_verified=False,
    )
    db.add(ev5a)
    db.flush()

    add_custody_chain(db, ev5a, [
        dict(performed_by=s_okafor.id, action=CustodyAction.COLLECTED, to_person=s_okafor.id,
             notes="Exported directly from platform admin console per Legal's written request (on file).",
             when=days_ago(2, 15, 10)),
    ])

    note5 = CaseNote(
        id=uuid4(), case_id=case5.id, author_id=s_okafor.id,
        note="Awaiting Legal sign-off before proceeding to endpoint/USB artifact review. Initial pass of clone logs shows no unusual volume relative to the engineer's normal baseline.",
        created_at=days_ago(2, 16, 30),
    )
    db.add(note5)

    # -----------------------------------------------------------------
    # Case 6 — Archived prior-year case
    # -----------------------------------------------------------------
    case6 = Case(
        id=uuid4(),
        case_number="CASE-2025-0038",
        title="Phishing-Initiated Wire Fraud — Accounts Payable",
        description=(
            "Business email compromise led to a fraudulent wire transfer approval. "
            "Investigation traced the initial phishing email, mailbox rule tampering, "
            "and confirmed the compromised account was the sole point of entry."
        ),
        status=CaseStatus.ARCHIVED,
        priority=CasePriority.HIGH,
        created_by=m_reyes.id,
        assigned_to=m_reyes.id,
        opened_at=days_ago(210, 8, 0),
        closed_at=days_ago(178, 17, 0),
    )
    case6.tags.extend([tag_network, tag_ediscovery])
    db.add(case6)

    ev6a = EvidenceItem(
        id=uuid4(),
        case_id=case6.id,
        acquired_by=m_reyes.id,
        evidence_tag="E-2025-0038-01",
        name="AP Mailbox — Full Export (.pst)",
        description="Full mailbox export for the compromised accounts payable coordinator account, including inbox rules and sign-in log correlation.",
        evidence_type=EvidenceType.DOCUMENT.value,
        source_path="\\\\forensics-nas\\cases\\2025-0038\\ap-mailbox.pst",
        acquisition_method=AcquisitionMethod.MANUAL.value,
        acquired_at=days_ago(209, 9, 0).isoformat(),
        sha256=fake_sha256("case6-ap-mailbox"),
        md5=fake_md5("case6-ap-mailbox"),
        size_bytes=4_724_464_128,
        is_verified=True,
    )
    db.add(ev6a)
    db.flush()

    add_custody_chain(db, ev6a, [
        dict(performed_by=m_reyes.id, action=CustodyAction.COLLECTED, to_person=m_reyes.id,
             notes="Exported via eDiscovery admin center under legal hold LH-2025-011.",
             when=days_ago(209, 9, 20)),
        dict(performed_by=m_reyes.id, action=CustodyAction.ARCHIVED, from_person=m_reyes.id, to_person=m_reyes.id,
             notes="Case closed and remediated; evidence archived per 7-year financial-fraud retention schedule.",
             when=days_ago(178, 17, 0)),
    ])

    note6 = CaseNote(
        id=uuid4(), case_id=case6.id, author_id=m_reyes.id,
        note="Root cause confirmed as credential phishing; MFA was not enrolled on the compromised account at the time. Findings delivered to Legal and Finance; case closed after remediation verified.",
        is_archived=True,
        created_at=days_ago(179, 10, 0),
    )
    db.add(note6)

    db.commit()
    db.close()
