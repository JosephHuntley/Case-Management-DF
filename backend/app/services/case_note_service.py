# case_note_service.py
from fastapi import HTTPException
from uuid import UUID
from app.models.user import User
from sqlalchemy.orm import Session
from app.models.case_note import CaseNote
from app.repositories.case_note_repository import CaseNoteRepository
from app.schemas.case_note import CaseNoteCreate, CaseNoteOut
from app.services.audit_service import AuditService


class CaseNoteService:
    @staticmethod
    def create_case_note(db: Session, payload: CaseNoteCreate, current_user: User) -> CaseNote:
        case_note = CaseNoteRepository(db).create_case_note(payload, current_user)

        audit_data = CaseNoteOut.model_validate(case_note).model_dump(mode="json")
        AuditService(db).log_create(
            entity_type="case_note",
            entity_id=case_note.id,
            user_id=current_user.id,
            new_values=audit_data
        )

        db.commit()
        db.refresh(case_note)
        return case_note

    @staticmethod
    def get_case_note_by_id(db: Session, case_note_id: UUID) -> CaseNote | None:
        response = CaseNoteRepository(db).get_case_note_by_id(case_note_id)
        if response is None:
            raise HTTPException(status_code=404, detail="Case note not found")
        return response

    @staticmethod
    def get_case_notes_by_case_id(db: Session, case_id: UUID) -> list[CaseNote]:
        return CaseNoteRepository(db).get_case_notes_by_case_id(case_id)

    @staticmethod
    def update_case_note(
        db: Session,
        case_note_id: UUID,
        updated_data: dict,
        current_user: User
    ) -> CaseNote | None:
        case_note = CaseNoteRepository(db).get_case_note_by_id(case_note_id)
        if not case_note:
            return None

        old_data = CaseNoteOut.model_validate(case_note).model_dump(mode="json")
        updated_case_note = CaseNoteRepository(db).update_case_note(case_note, updated_data, current_user)
        new_data = CaseNoteOut.model_validate(updated_case_note).model_dump(mode="json")

        AuditService(db).log_update(
            entity_type="case_note",
            entity_id=case_note.id,
            user_id=current_user.id,
            old_values=old_data,
            new_values=new_data
        )

        db.commit()
        db.refresh(updated_case_note)
        return updated_case_note

    @staticmethod
    def archive_case_note(
        db: Session,
        case_note_id: UUID,
        current_user: User
    ) -> CaseNote | None:
        case_note = CaseNoteRepository(db).get_case_note_by_id(case_note_id)
        if not case_note:
            return None

        audit_data = CaseNoteOut.model_validate(case_note).model_dump(mode="json")
        archived_case_note = CaseNoteRepository(db).archive_case_note(case_note, current_user)

        AuditService(db).log_delete(
            entity_type="case_note",
            entity_id=case_note.id,
            user_id=current_user.id,
            old_values=audit_data
        )

        db.commit()
        db.refresh(archived_case_note)
        return case_note