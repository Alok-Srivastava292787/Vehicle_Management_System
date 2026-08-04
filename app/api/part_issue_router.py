from fastapi import (    APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import ( Session,)

from app.db.dependencies import (    get_db,)

from app.repositories.part_issue_repository import (    PartIssueRepository,)
from app.schemas.part_issue_schema import (
    PartIssueCreate,
    PartIssueUpdate,
)
from app.repositories.part_requisition_repository import (    PartRequisitionRepository,)
from app.services.part_issue_service import (    PartIssueService,)
from app.repositories.part_requisition_detail_repository import (    PartRequisitionDetailRepository,)
from app.repositories.part_issue_detail_repository import (    PartIssueDetailRepository,)

router = APIRouter(
    prefix="/api/v1/part-issues",
    tags=["Part Issues"],
)


def get_service(
    db: Session =
    Depends(get_db),
):

    return (
        PartIssueService(
            repository=
                PartIssueRepository(db),
            requisition_repository=
                PartRequisitionRepository(db),
            requisition_detail_repository=
                PartRequisitionDetailRepository(db),
            issue_detail_repository=
                PartIssueDetailRepository(db),
        )
    )


@router.post("")
def create_part_issue(
    payload:
    PartIssueCreate,

    service:
    PartIssueService =
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
def get_part_issues(
    service:
    PartIssueService =
    Depends(
        get_service
    ),
):

    return (
        service.get_all()
    )


@router.get(
    "/{issue_id}"
)
def get_part_issue(
    issue_id: int,

    service:
    PartIssueService =
    Depends(
        get_service
    ),
):

    return (
        service.get_by_id(
            issue_id
        )
    )


@router.put(
    "/{issue_id}"
)
def update_part_issue(
    issue_id: int,

    payload:
    PartIssueUpdate,

    service:
    PartIssueService =
    Depends(
        get_service
    ),
):

    return (
        service.update(
            issue_id,
            payload,
        )
    )


@router.delete(
    "/{issue_id}"
)
def delete_part_issue(
    issue_id: int,

    service:
    PartIssueService =
    Depends(
        get_service
    ),
):

    return (
        service.delete(
            issue_id
        )
    )


@router.post(
    "/create-from-requisition/{requisition_id}"
)
def create_from_requisition(
    requisition_id: int,
    service:
    PartIssueService =
    Depends(get_service),
):
    return (
        service.create_from_requisition(
            requisition_id
        )
    )
