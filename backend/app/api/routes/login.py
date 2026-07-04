from app.db.session import get_db
from app.models import User, AuthEventType
from app.security import verify_password, create_access_token
from app.services import AuthService
from app.core.config import settings


from fastapi import APIRouter, Depends, HTTPException, Response
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
def login(
    request:Request, 
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db),
    ):

    user = db.query(User).filter(
        User.username == form_data.username,
        User.is_active == True
    ).first()

    if not user or not verify_password(form_data.password, user.password_hash):
        reason = AuthEventType.INVALID_USER.value if not user else AuthEventType.INVALID_PASSWORD.value
        ip = request.client.host
        agent = request.headers.get("user-agent", "unknown")

        AuthService.log_failed_login(db, username=form_data.username, ip_addr=ip, agent=agent, reason=reason)

        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    tokens = AuthService.issue_tokens(db, user)

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/auth",  
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh")
def refresh(request: Request, response: Response, db: Session = Depends(get_db)):
    raw_refresh_token = request.cookies.get("refresh_token")
    if not raw_refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token provided")

    tokens = AuthService.refresh_access_token(db, raw_refresh_token)

    response.set_cookie(
        key="refresh_token",
        value=tokens["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        path="/api/auth",
    )

    return {"access_token": tokens["access_token"], "token_type": "bearer"}

# TODO Implement logout endpoint that revokes the refresh token and clears the cookie
# @router.post("/logout")
# def logout(request: Request, response: Response, db: Session = Depends(get_db)):
#     refresh_token = request.cookies.get("refresh_token")
#     if refresh_token:
#         revoke_refresh_token(db, refresh_token)  

#     response.delete_cookie(key="refresh_token", path="/api/auth")
#     return {"detail": "Logged out"}