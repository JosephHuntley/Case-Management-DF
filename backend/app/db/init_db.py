from app.db.base import Base
from app.db.session import engine

from app.db.models.case import Case
from app.db.models.user import User
from app.db.models.case_note import CaseNote
from app.db.models.evidence_item import EvidenceItem
from app.db.models.chain_of_custody import ChainOfCustody
from app.db.models.tag import Tag
from app.db.models.case_tag import CaseTag

def init_db():
    Base.metadata.create_all(bind=engine)