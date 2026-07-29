from fastapi import ( APIRouter, Depends,)  #type: ignore

from sqlalchemy.orm import (
    Session,
)

from app.repositories.part_issue_repository import (
    PartIssueRepository,
)

from app.repositories.part_requisition_detail_repository import (
    PartRequisitionDetailRepository,
)

from app.db.dependencies import (
    get_db,
)

from app.repositories.part_issue_detail_repository import (
    PartIssueDetailRepository,
)

from app.schemas.part_issue_detail_schema import (
    PartIssueDetailCreate,
    PartIssueDetailUpdate,
)

from app.services.part_issue_detail_service import (
    PartIssueDetailService,
)
from app.repositories.stock_ledger_repository import    (   StockLedgerRepository)

router = APIRouter(
    prefix="/api/v1/part-issue-details",
    tags=["Part Issue Details"],
)


def get_service(
    db: Session =
    Depends(get_db),
):

    return (
        PartIssueDetailService(
        repository=PartIssueDetailRepository(db),
        issue_repository=PartIssueRepository(db),
        requisition_detail_repository=PartRequisitionDetailRepository(db),
        stock_ledger_repository=StockLedgerRepository(db),
        )
    )

@router.post("")
def create_part_issue_detail(
    payload:
    PartIssueDetailCreate,

    service:
    PartIssueDetailService =
    Depends(
        get_service
    ),
):
    return (
        service.create(
            payload
        )
    )


@router.get("")
def get_part_issue_details(
    service:
    PartIssueDetailService =
    Depends(
        get_service
    ),
):
    return (
        service.get_all()
    )


@router.get(
    "/{issue_detail_id}"
)
def get_part_issue_detail(
    issue_detail_id: int,

    service:
    PartIssueDetailService =
    Depends(
        get_service
    ),
):
    return (
        service.get_by_id(
            issue_detail_id
        )
    )


@router.put(
    "/{issue_detail_id}"
)
def update_part_issue_detail(
    issue_detail_id: int,

    payload:
    PartIssueDetailUpdate,

    service:
    PartIssueDetailService =
    Depends(
        get_service
    ),
):
    return (
        service.update(
            issue_detail_id,
            payload,
        )
    )


@router.delete(
    "/{issue_detail_id}"
)
def delete_part_issue_detail(
    issue_detail_id: int,

    service:
    PartIssueDetailService =
    Depends(
        get_service
    ),
):
    return (
        service.delete(
            issue_detail_id
        )
    )