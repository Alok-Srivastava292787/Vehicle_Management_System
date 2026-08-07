from fastapi import (    APIRouter,    Depends,)    #type: ignore

from fastapi.responses import (    StreamingResponse,)  #type: ignore

from sqlalchemy.orm import Session

from app.db.dependencies import (
    get_db,
)

from app.repositories.part_issue_repository import (
    PartIssueRepository,
)

from app.repositories.part_issue_detail_repository import (
    PartIssueDetailRepository,
)

from app.repositories.employee_repository import (
    EmployeeRepository,
)
from app.repositories.part_requisition_repository import (PartRequisitionRepository)
from app.repositories.part_repository import (
    PartRepository,
)

from app.services.pdf_issue_service import (
    PDFIssueService,
)

router = APIRouter(
    prefix="/api/v1/issue_print",
    tags=["Part Issue PDF"],
)


@router.get(
    "/{issue_id}/pdf"
)
def generate_issue_pdf(
    issue_id: int,
    db: Session = Depends(get_db),
):

    issue_repo = ( PartIssueRepository(db))

    issue = (issue_repo.get_by_id(issue_id))

    if not issue:
        return {
            "message":
            "Issue not found"
        }

    detail_repo = (PartIssueDetailRepository(db))

    details = [
        item
        for item in detail_repo.get_all()
        if item.issue_id
        == issue_id
    ]

    employee_repo = (EmployeeRepository(db))
    issued_by = None
    received_by = None
    if issue.issued_by_employee_id:
        issued_by = (
            employee_repo.get_by_id(
                issue.issued_by_employee_id
            )
        )
    if issue.received_by_employee_id:

        received_by = (
            employee_repo.get_by_id(
                issue.received_by_employee_id
            )
        )

    part_lookup = {}

    part_repo = (
        PartRepository(db)
    )

    for detail in details:

        part = (
            part_repo.get_by_id(
                detail.part_id
            )
        )

        if part:

            part_lookup[
                detail.part_id
            ] = (
                part.part_name
            )
    requisition_repository=PartRequisitionRepository(db)
    requisition =requisition_repository.get_by_id(issue.requisition_id)
    setattr(
    issue,
    "requisition_number",
    requisition.requisition_number
    if requisition
    else None,
    )

    setattr(
        issue,
        "job_card_id",
        requisition.job_card_id
        if requisition
        else None,
    )
    pdf = (
        PDFIssueService
        .generate_issue_pdf(
            issue,
            issued_by,
            received_by,
            details,
            part_lookup,
        )
    )

    return StreamingResponse(
        pdf,
        media_type=
        "application/pdf",
        headers={
            "Content-Disposition":
            (
                f'inline; filename="issue_{issue_id}.pdf"'
            )
        },
    )