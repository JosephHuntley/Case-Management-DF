from app.models import User, UserRole
from app.security import get_current_user, require_role
from app.services import TagService
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas import TagCreate, TagOut

router = APIRouter(prefix="/tags", tags=["Tags"])

# Create
@router.post("/", response_model=TagOut)
def create_tag(payload: TagCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role (UserRole.ADMIN, UserRole.INVESTIGATOR))):
    
    return TagService.create_tag(db, payload, current_user)

# Read all
@router.get("/", response_model=list[TagOut])
def get_tags(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return TagService.get_tags(db)

# Update
@router.put("/{tag_id}", response_model=TagOut)
def update_tag(tag_id: str, payload: TagCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role (UserRole.ADMIN, UserRole.INVESTIGATOR))):
    return TagService.update_tag(db, tag_id, payload, current_user)

# Delete
@router.delete("/{tag_id}")
def delete_tag(tag_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role (UserRole.ADMIN, UserRole.INVESTIGATOR))):
    if TagService.delete_tag(db, tag_id, current_user):
        return {"detail": "Tag deleted successfully"}