
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.services import CaseService
from app.db.session import get_db
from app.schemas import CaseCreate, CaseUpdate, CaseOut
from app.security import get_current_user

router = APIRouter(prefix="/cases", tags=["Cases"])


# CREATE
@router.post("/", response_model=CaseOut)
def create_case(
    payload: CaseCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return CaseService.create_case(db, payload, current_user)


# READ ALL
@router.get("/", response_model=list[CaseOut])
def get_cases(
    db: Session = Depends(get_db)
):
    return CaseService.get_cases(db)

# READ ONE
@router.get("/{case_id}", response_model=CaseOut)
def get_case(
    case_id: str,
    db: Session = Depends(get_db)
):
    case = CaseService.get_case(db, case_id)

    if not case:
        raise HTTPException(
            status_code=404,
            detail="Case not found"
        )

    return case


# UPDATE
@router.put("/{case_id}", response_model=CaseOut)
def update_case(case_id: str, payload: CaseUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    case = CaseService.get_case(db, case_id)

    return CaseService.update_case(db, case_id, payload, current_user)


# SOFT DELETE
@router.delete("/{case_id}")
def delete_case(case_id: str, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
  
    return CaseService.delete_case(db, case_id, current_user)

