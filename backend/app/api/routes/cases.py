from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from uuid import uuid4
from datetime import datetime

from app.db.session import get_db
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate, CaseOut
from app.models.tag import Tag

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
        created_by=payload.created_by
    )

    if payload.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(payload.tag_ids)).all()
        case.tags = tags

    db.add(case)
    db.commit()
    db.refresh(case)
    return case


# READ ALL
@router.get("/", response_model=list[CaseOut])
def get_cases(db: Session = Depends(get_db)):
    return (
        db.query(Case)
        .options(selectinload(Case.tags))
        .filter(Case.deleted_at.is_(None))
        .all( ))


# READ ONE
@router.get("/{case_id}", response_model=CaseOut)
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).options(selectinload(Case.tags)).filter(Case.id == case_id).first()

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
    
    update_data = payload.model_dump(exclude_unset=True)

    tag_ids = update_data.pop("tag_ids", None)

    for key, value in update_data.items():
        setattr(case, key, value)

    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

        print("Requested:", tag_ids)
        print("Found:", [str(t.id) for t in tags])

        case.tags = tags
    
    db.commit()
    db.refresh(case)
    return case


# SOFT DELETE
@router.delete("/{case_id}")
def delete_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    case.deleted_at = datetime.utcnow()

    db.commit()
    return {"message": "case archived"}