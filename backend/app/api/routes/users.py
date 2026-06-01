from app.services.user_service import UserService
from app.security import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserOut

router = APIRouter(prefix="/users", tags=["Users"])

# CREATE
@router.post("/", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):   
    return UserService.create_user(db, payload, current_user)

# READ ALL
@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return UserService.get_all_users(db)

# READ ONE
@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = UserService.get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="No users found"
        )
    return user

# UPDATE
@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: str, payload: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserService.update_user(db, user_id, payload, current_user)

# SOFT DELETE
@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return UserService.delete_user(db, user_id, current_user)