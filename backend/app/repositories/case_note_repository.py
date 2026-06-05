from uuid import UUID, uuid4
from datetime import datetime
from app.models.user import User
from sqlalchemy.orm import Session

from app.schemas.case_note import CaseNoteCreate
from app.models.case_note import CaseNote


class CaseNoteRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_case_note(self, case_note: CaseNoteCreate, current_user: User) -> CaseNote:
        new_case_note = CaseNote(
            id=uuid4(),
            case_id=case_note.case_id,
            author_id=current_user.id,
            note=case_note.note,
            updated_by=current_user.id
        )
        self.db.add(new_case_note)
        self.db.flush()
        return new_case_note
    
    def get_case_note_by_id(self, case_note_id: UUID) -> CaseNote | None:
        return self.db.query(CaseNote).filter(CaseNote.id == case_note_id).first()
    
    def get_case_notes_by_case_id(self, case_id: UUID) -> list[CaseNote]:
        return self.db.query(CaseNote).filter(CaseNote.case_id == case_id, CaseNote.is_archived == False).all()
    
    def update_case_note(self, case_note: CaseNote, updated_data: dict, current_user: User) -> CaseNote:
        for key, value in updated_data.items():
            setattr(case_note, key, value)
        case_note.updated_by = current_user.id
        self.db.flush()
        return case_note
    
    def archive_case_note(self, case_note: CaseNote, current_user: User) -> CaseNote:
        case_note.is_archived = True
        case_note.updated_by = current_user.id
        self.db.flush()
        return case_note
    