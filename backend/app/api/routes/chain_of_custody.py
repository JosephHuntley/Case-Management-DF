from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.security import get_current_user, require_role
from app.services import ChainOfCustodyService
from app.models import User, UserRole
from app.schemas import ChainOfCustodyCreate, ChainOfCustodyOut

router = APIRouter(prefix="/chain-of-custody", tags=["Chain of Custody"])

# CREATE
@router.post("/", response_model=ChainOfCustodyOut)
def create_chain_of_custody(
    payload: ChainOfCustodyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role (UserRole.ADMIN, UserRole.INVESTIGATOR))
):
    return ChainOfCustodyService.create_chain_of_custody(db, payload, current_user)

# READ by ID
@router.get("/{chain_of_custody_id}", response_model=ChainOfCustodyOut)
def get_chain_of_custody_by_id(
    chain_of_custody_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return ChainOfCustodyService.get_chain_of_custody_by_id(db, chain_of_custody_id)    

# READ by Evidence ID
@router.get("/evidence/{evidence_id}", response_model=ChainOfCustodyOut)
def get_chain_of_custody_by_evidence_id(
    evidence_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return ChainOfCustodyService.get_chain_of_custody_by_evidence_id(db, evidence_id)
