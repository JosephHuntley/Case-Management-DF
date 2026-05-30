from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from app.db.session import get_db
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate, CaseOut

router = APIRouter(prefix="/cases", tags=["Cases"])


# CREATE
@router.post("/", response_model=CaseOut)
def create_case(payload: CaseCreate, db: Session = Depends(get_db)):
    case = Case(
        id=uuid4(),
        case_number=str(uuid4())[:8],
        title=payload.title,
        description=payload.description,
        status=payload.status,
        priority=payload.priority,
    )

    db.add(case)
    db.commit()
    db.refresh(case)
    return case


# READ ALL
@router.get("/", response_model=list[CaseOut])
def get_cases(db: Session = Depends(get_db)):
    return db.query(Case).filter(Case.deleted_at.is_(None)).all()


# READ ONE
@router.get("/{case_id}", response_model=CaseOut)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    return case


# UPDATE
@router.put("/{case_id}", response_model=CaseOut)
def update_case(case_id: str, payload: CaseUpdate, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    for key, value in payload.dict(exclude_unset=True).items():
        setattr(case, key, value)

    db.commit()
    db.refresh(case)
    return case


# SOFT DELETE
@router.delete("/{case_id}")
def delete_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    case.deleted_at = case.deleted_at or None
    from datetime import datetime
    case.deleted_at = datetime.utcnow()

    db.commit()
    return {"message": "case archived"}