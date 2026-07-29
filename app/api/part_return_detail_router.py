from fastapi import (    APIRouter,Depends,)    #type: ignore

from sqlalchemy.orm import Session

from app.db.dependencies import get_db

from app.repositories.part_return_detail_repository import (
    PartReturnDetailRepository,
)

from app.schemas.part_return_detail_schema import (
    PartReturnDetailCreate,
    PartReturnDetailUpdate,
)

from app.services.part_return_detail_service import (
    PartReturnDetailService,
)
from app.repositories.part_issue_detail_repository import   (PartIssueDetailRepository)
from app.repositories.part_return_repository import (PartReturnRepository)
from app.repositories.stock_ledger_repository import    (   StockLedgerRepository)


router = APIRouter(
    prefix="/api/v1/part-return-details",
    tags=["Part Return Details"],
)


def get_service(
    db: Session = Depends(get_db),
):

    return (PartReturnDetailService(
        repository=PartReturnDetailRepository(db),
        return_repository=PartReturnRepository(db),
        issue_detail_repository=PartIssueDetailRepository(db),
        stock_ledger_repository=StockLedgerRepository(db),
            )
        )

@router.post("")
def create_part_return_detail(
    payload: PartReturnDetailCreate,
    service: PartReturnDetailService = Depends(get_service),
):
    return service.create(payload)


@router.get("")
def get_part_return_details(
    service: PartReturnDetailService = Depends(get_service),
):
    return service.get_all()


@router.get("/{return_detail_id}")
def get_part_return_detail(
    return_detail_id: int,
    service: PartReturnDetailService = Depends(get_service),
):
    return service.get_by_id(return_detail_id)


@router.put("/{return_detail_id}")
def update_part_return_detail(
    return_detail_id: int,
    payload: PartReturnDetailUpdate,
    service: PartReturnDetailService = Depends(get_service),
):
    return service.update(
        return_detail_id,
        payload,
    )


@router.delete("/{return_detail_id}")
def delete_part_return_detail(
    return_detail_id: int,
    service: PartReturnDetailService = Depends(get_service),
):
    return service.delete(
        return_detail_id
    )