from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security import get_current_user
from app.services import ChainOfCustodyService
from app.models import User
from app.schemas import ChainOfCustodyCreate, ChainOfCustodyOut

router = APIRouter(prefix="/chain-of-custody", tags=["Chain of Custody"])

# CREATE
@router.post("/", response_model=ChainOfCustodyOut)
def create_chain_of_custody(
    payload: ChainOfCustodyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return ChainOfCustodyService.create_chain_of_custody(db, payload, current_user)

# READ by ID
@router.get("/{chain_of_custody_id}", response_model=list[ChainOfCustodyOut])
def get_chain_of_custody_by_id(
    chain_of_custody_id: str,
    db: Session = Depends(get_db)
):
    return ChainOfCustodyService.get_chain_of_custody_by_id(db, chain_of_custody_id)    

# READ by Evidence ID
@router.get("/evidence/{evidence_id}", response_model=list[ChainOfCustodyOut])
def get_chain_of_custody_by_evidence_id(
    evidence_id: str,
    db: Session = Depends(get_db)
):
    return ChainOfCustodyService.get_chain_of_custody_by_evidence_id(db, evidence_id)
