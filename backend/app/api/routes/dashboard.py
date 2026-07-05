from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, case as sql_case
from sqlalchemy.orm import Session
 
from app.db.session import get_db
from app.models import Case, EvidenceItem, User
from app.security import get_current_user
 
router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])
 
 
class DashboardSummary(BaseModel):
    active_cases: int
    total_cases: int
    evidence_items_total: int
    pending_reviews: int
 
 
@router.get("/summary", response_model=DashboardSummary)
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    case_query = db.query(
        func.count(Case.id).label("total"),
        func.sum(sql_case((Case.status == "open", 1), else_=0)).label("active"),
    )
 
    # --- If dashboard stats should be scoped to the current user's own
    # cases rather than org-wide, filter here instead (adjust the field
    # name to whatever links a Case to its owning investigator):
    #
    # if current_user.role != "admin":
    #     case_query = case_query.filter(Case.investigator_id == current_user.id)
 
    case_counts = case_query.one()
 
    evidence_total = db.query(func.count(EvidenceItem.id)).scalar()
 
    
    # TODO: Implement Report field 
    pending_reviews = 0
    # pending_reviews = (
    #     db.query(func.count(Report.id))
    #     .filter(Report.status == "draft")
    #     .scalar()
    # )
 
    return DashboardSummary(
        active_cases=case_counts.active or 0,
        total_cases=case_counts.total or 0,
        evidence_items_total=evidence_total or 0,
        pending_reviews=pending_reviews or 0,
    )
