from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import EvidenceItemOut, EvidenceItemCreate, EvidenceItemUpdate
from app.db.session import get_db
from app.security import get_current_user
from app.services import EvidenceService
from app.models import EvidenceItem

router = APIRouter(prefix="/evidence-items", tags=["Evidence Items"])

# Create
@router.post("/", response_model=EvidenceItemOut)
def create_evidence(payload: EvidenceItemCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> EvidenceItem:
    return EvidenceService.create_evidence(db, payload, current_user)

# Read
@router.get("/{item_id}", response_model=EvidenceItemOut)
def get_evidence_by_id(item_id: str, db: Session = Depends(get_db)) -> EvidenceItem:
    return EvidenceService.get_by_id(db, item_id)

# Read by Case
@router.get("/case/{case_id}", response_model=list[EvidenceItemOut])
def get_evidence_by_case_id(case_id:str, db: Session = Depends(get_db)) -> list[EvidenceItem]:
    return EvidenceService.get_by_case_id(db, case_id)

# Update Evidence 
@router.put("/{item_id}", response_model=EvidenceItemOut)
def update_item(item_id:str, payload: EvidenceItemUpdate, db:Session = Depends(get_db), current_user: str = Depends(get_current_user)) -> EvidenceItem:
    return EvidenceService.update_evidence(db, item_id, payload, current_user) 