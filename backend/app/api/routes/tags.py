from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime

from app.db.session import get_db

from app.models.tag import Tag
from app.schemas.tag import TagCreate, TagOut

router = APIRouter(prefix="/tags", tags=["Tags"])

# Create
@router.post("/", response_model=TagOut)
def create_tag(payload: TagCreate, db: Session = Depends(get_db)):
    tag = Tag(
        id=str(uuid4()),
        name=payload.name,
        description=payload.description,
        created_at=datetime.utcnow(),
        color=payload.color
    )

    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag

# Read all
@router.get("/", response_model=list[TagOut])
def get_tags(db: Session = Depends(get_db)):
    tags = db.query(Tag).all()
    return tags

# Update
@router.put("/{tag_id}", response_model=TagOut)
def update_tag(tag_id: str, payload: TagCreate, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    tag.name = payload.name
    tag.description = payload.description
    tag.color = payload.color
    db.commit()
    db.refresh(tag)
    return tag

# Delete
@router.delete("/{tag_id}")
def delete_tag(tag_id: str, db: Session = Depends(get_db)):
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")

    db.delete(tag)
    db.commit()
    return {"detail": "Tag deleted successfully"}