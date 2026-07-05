from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, case as sql_case
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import Case, EvidenceItem, User
from app.security import get_current_user
from app.repositories import ChainOfCustodyRepository

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


class DashboardSummary(BaseModel):
    active_cases: int
    total_cases: int
    evidence_items_total: int
    pending_reviews: int
    custody_integrity_percent: int


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

    evidence_ids = [row[0] for row in db.query(EvidenceItem.id).all()]
    evidence_total = len(evidence_ids)

    # NOTE: this runs one verification pass per evidence item (N queries
    # total). Fine at this app's current scale; if evidence volume grows
    # significantly, this is worth caching or moving to a background job
    # that updates a stored percentage instead of recomputing on every
    # dashboard load.
    #
    # Uses the repository directly (not ChainOfCustodyService), since the
    # service raises a 404 for evidence items with zero custody entries —
    # correct behavior for a single-evidence-item API response, but wrong
    # for this aggregate: an item with no custody entries yet has nothing
    # to contradict, so it's counted as valid (entry_count == 0, is_valid
    # stays True) rather than excluded or treated as broken. Worth
    # reconsidering if "no custody record at all" should actually count
    # against the integrity percentage instead.
    if evidence_ids:
        repo = ChainOfCustodyRepository(db)
        valid_count = sum(
            1 for eid in evidence_ids
            if repo.verify_chain_of_custody(eid)["is_valid"]
        )
        custody_integrity_percent = round((valid_count / evidence_total) * 100)
    else:
        custody_integrity_percent = 100

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
        custody_integrity_percent=custody_integrity_percent,
    )