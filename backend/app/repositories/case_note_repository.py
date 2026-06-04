from uuid import UUID, uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from app.schemas.case_note import CaseNoteCreate
from app.models.case_note import CaseNote


class CaseNoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_case_note(self, case_note: CaseNoteCreate) -> CaseNote:
        new_case_note = CaseNote(
            id=uuid4(),
            case_id=case_note.case_id,
            author_id=case_note.author_id,
            content=case_note.content,
            created_at=datetime.utcnow(),
        )
        self.db.add(new_case_note)
        self.db.commit()
        self.db.refresh(new_case_note)
        return new_case_note