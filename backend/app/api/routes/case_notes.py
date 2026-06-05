from app.schemas.case_note import CaseNoteCreate, CaseNoteOut
from app.db.session import get_db
from app.security import get_current_user
from app.services.case_note_service import CaseNoteService
from app.models.user import User
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session


router = APIRouter(prefix="/case-notes", tags=["Case Notes"])

# CREATE
@router.post("/", response_model=CaseNoteOut)
def create_case_note(
    payload: CaseNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CaseNoteService.create_case_note(db, payload, current_user)

# READ
@router.get("/{case_note_id}", response_model=CaseNoteOut)
def get_case_note_by_id(
    case_note_id: str,
    db: Session = Depends(get_db)
):
    return CaseNoteService.get_case_note_by_id(db, case_note_id)

# READ ALL BY CASE ID
@router.get("/case/{case_id}", response_model=list[CaseNoteOut])
def get_case_notes_by_case_id(
    case_id: str,
    db: Session = Depends(get_db)
):
    return CaseNoteService.get_case_notes_by_case_id(db, case_id)

# UPDATE
@router.put("/{case_note_id}", response_model=CaseNoteOut)
def update_case_note(
    case_note_id: str,
    updated_data: CaseNoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CaseNoteService.update_case_note(db, case_note_id, updated_data.dict(exclude_unset=True), current_user)

# DELETE (ARCHIVE)
@router.delete("/{case_note_id}", response_model=CaseNoteOut)
def archive_case_note(
    case_note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return CaseNoteService.archive_case_note(db, case_note_id, current_user)