from app.db.base import Base
from app.db.session import engine

from ..models.case import Case
from ..models.user import User
from ..models.case_note import CaseNote
from ..models.evidence_item import EvidenceItem
from ..models.chain_of_custody import ChainOfCustody
from ..models.tag import Tag
from ..models.case_tag import CaseTag
from ..models.audit_log import AuditLog
from ..models.report import Report

def init_db():
    Base.metadata.create_all(bind=engine)