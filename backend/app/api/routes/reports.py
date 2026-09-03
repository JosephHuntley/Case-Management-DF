from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse

from app.services import ReportService
from app.db.session import get_db
from app.security import get_current_user

router = APIRouter( tags=["Reports"])

# Get Case Report
@router.get("/cases/{case_id}/report")
def get_case_report(
    case_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    pdf = ReportService.get_case_report(db, case_id, current_user)

    return StreamingResponse(
        pdf,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=case-report.pdf"
        },
    )