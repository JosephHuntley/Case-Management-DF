from pydantic import BaseModel
from uuid import UUID
from typing import Any, Optional
from app.models import AuthEventType

class AuthLogCreate(BaseModel):
    username_attempted:str
    ip_addr:str
    user_agent:str 
    event_type: AuthEventType

    