from typing import Literal
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Case, EvidenceItem
from app.security import get_current_user, User

router = APIRouter(prefix="/api/search", tags=["search"])

RESULT_LIMIT = 10


class SearchResult(BaseModel):
    type: Literal["case", "evidence"]
    id: str
    label: str          
    title: str           
    case_id: str | None = None 


@router.get("/", response_model=list[SearchResult])
def search(
    q: str = Query(..., min_length=1, max_length=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    term = f"%{q}%"
    results: list[SearchResult] = []

    cases = (
        db.query(Case)
        .filter(or_(Case.case_number.ilike(term), Case.title.ilike(term)))
        .limit(RESULT_LIMIT)
        .all()
    )
    results.extend(
        SearchResult(type="case", id=str(c.id), label=c.case_number, title=c.title)
        for c in cases
    )

    evidence = (
        db.query(EvidenceItem)
        .filter(
            or_(
                EvidenceItem.evidence_tag.ilike(term),
                EvidenceItem.name.ilike(term),
                EvidenceItem.description.ilike(term),
            )
        )
        .limit(RESULT_LIMIT)
        .all()
    )
    results.extend(
        SearchResult(
            type="evidence",
            id=str(e.id),
            label=e.evidence_tag,
            title=e.description,
            case_id=str(e.case_id),
        )
        for e in evidence
    )

    # Combined cap in case both queries individually hit RESULT_LIMIT
    return results[:RESULT_LIMIT]