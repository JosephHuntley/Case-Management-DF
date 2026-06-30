from app.db.session import get_db
from app.models import User
from app.security import verify_password, create_access_token
from app.services.auth_service import AuthService
from app.core.config import settings

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from fastapi import Request
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["login"])

class RefreshRequest(BaseModel):
    refresh_token: str

@router.post("/login", status_code=200)
@limiter.limit("5/minute", exempt_when=lambda: not settings.RATE_LIMIT_ENABLED)
def login(request:Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username, User.is_active).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return AuthService.issue_tokens(db, user)

@router.post("/refresh")
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    return AuthService.refresh_access_token(db, payload.refresh_token)