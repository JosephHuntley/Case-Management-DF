from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.services import UserService
from app.security import get_current_user, require_role, require_self_or_role
from app.db.session import get_db
from app.models import User, UserRole
from app.schemas import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

# CREATE
@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(require_role (UserRole.ADMIN, UserRole.INVESTIGATOR))):   
    return UserService.create_user(db, payload, current_user)

# READ ALL
@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    return UserService.get_all_users(db)

# READ ONE
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db),current_user: str = Depends(get_current_user)):
    user = UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No users found"
        )
    return user

# UPDATE
@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_self_or_role( UserRole.ADMIN))):
    return UserService.update_user(db, user_id, payload, current_user)

# UPDATE
@router.put("/role/{user_id}", response_model=UserOut)
def update_user_role(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_role( UserRole.ADMIN))):
    return UserService.update_user_role(db, user_id, payload, current_user)

# SOFT DELETE
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(require_role (UserRole.ADMIN))):
    return UserService.delete_user(db, user_id, current_user)