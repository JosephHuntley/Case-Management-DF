from sqlalchemy.orm import Session
from io import BytesIO
from fastapi.responses import StreamingResponse
from fastapi import HTTPException

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)

from app.models import CustodyAction
from app.services import CaseService

class ReportService:
    # TODO: Add coverpage with logo
    # TODO: Add table of contents
    # TODO: Add page header
    # TODO: Look into adding a watermark to the report
    
    
    @staticmethod
    def get_case_report(db: Session, case_id: str, current_user: str):
        case = CaseService.get_case(db, case_id)

        if not case:
            raise HTTPException(
                status_code=404,
                detail="Case not found"
            )
        
        buffer = BytesIO()

        document = SimpleDocTemplate(
            buffer,
            pagesize=letter,
        )

        styles = getSampleStyleSheet()

        subtext = ParagraphStyle(
            "Subtext",
            parent=styles["Normal"],
            fontName="Helvetica-Oblique",
            fontSize=6,
        )

        content = [
            Paragraph(
                "Digital Forensic Case Report",
                styles["Title"]
            ),
            Paragraph(
                f"Generated on: {case.created_at.strftime('%Y-%m-%d %H:%M:%S')} by {current_user.first_name} {current_user.last_name} ({current_user.email})",
                styles["Normal"]
            ),
            Spacer(1, 20),

            Paragraph(
                "Case Details:",
                styles["Heading2"]
            ),
            Paragraph(
                "Case Title: " + case.title,
                styles["Normal"]
            ),
            Paragraph(
                "Case Number: " + case.case_number,
                styles["Normal"]
            ),
            Paragraph(
                "Lead Investigator: "
                + f"{case.assignee.first_name} "
                + f"{case.assignee.last_name} "
                + f"({case.assignee.email})",
                styles["Normal"]
            ),
            Paragraph(
                "Status: " + case.status,
                styles["Normal"]
            ),
            Paragraph(
                "Description: " + case.description,
                styles["Normal"]
            ),

            Spacer(1, 20),

            Paragraph(
                "Case Notes:",
                styles["Heading2"]
            ),
        ]

        for note in case.notes:
            content.append(
                Paragraph(
                    f"{note.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {note.note}",
                    styles["Normal"]
                )
            )

        content.append(Spacer(1, 20))

        content.append(
            Paragraph(
                "Evidence Items:",
                styles["Heading2"]
            )
        )

        for evidence in case.evidence_items:
            content.append(
                Paragraph(
                    f"{evidence.name} - {evidence.description}",
                    styles["Normal"]
                )
            )
            content.append(
                Paragraph(
                    f"Tag: {evidence.evidence_tag}",
                    styles["Normal"]
                )
            )
        
        content.append(
            Paragraph(
                "Chain of Custody:",
                styles["Heading2"]
            )
        )

        for evidence in case.evidence_items:
            content.append(
                Paragraph(
                    f"{evidence.name} - Chain of Custody",
                    styles["Heading3"]
                )
            )

            for chain in evidence.custody_chain:
                if chain.action == CustodyAction.COLLECTED:
                    content.append(
                        Paragraph(
                            f"{chain.created_at.strftime('%Y-%m-%d %H:%M:%S')} - "
                            + f"{chain.action.value} by {chain.to_person_user.first_name} "
                            + f"{chain.to_person_user.last_name} ({chain.to_person_user.email})",
                            styles["Normal"]
                        )
                    )
                else:
                    content.append(
                        Paragraph(
                            f"{chain.created_at.strftime('%Y-%m-%d %H:%M:%S')} - "
                            + f"{chain.action.value} by {chain.from_person_user.first_name} "
                            + f"{chain.from_person_user.last_name} ({chain.from_person_user.email})",
                            styles["Normal"]
                        )
                    )
                content.append(
                    Paragraph(
                        f"Logged by: {chain.performer.first_name} {chain.performer.last_name} ({chain.performer.email})",
                        subtext
                    )
                )
        

        document.build(content)

        buffer.seek(0)

        return buffer