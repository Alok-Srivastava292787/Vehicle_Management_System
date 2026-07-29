from fastapi import HTTPException   #type: ignore

from app.models.part_return import (
    PartReturnDetail,
)

from app.repositories.part_return_detail_repository import (
    PartReturnDetailRepository,
)
from app.repositories.part_issue_detail_repository import   (PartIssueDetailRepository)
from app.repositories.part_return_repository import (PartReturnRepository)
from app.repositories.stock_ledger_repository import (StockLedgerRepository,)
from app.services.stock_ledger_service import (StockLedgerService,)


class PartReturnDetailService:

    def __init__(
        self,
        repository: PartReturnDetailRepository,
        return_repository: PartReturnRepository,
        issue_detail_repository: PartIssueDetailRepository,
        stock_ledger_repository: StockLedgerRepository,
    ):
        self.repository = repository
        self.return_repository = return_repository
        self.issue_detail_repository = issue_detail_repository
        self.stock_ledger_repository = stock_ledger_repository

    def validate_quantity_returned(
        self,
        return_id: int,
        part_id: int,
        quantity_returned: float,
    ):
        return_header = (
            self.return_repository
            .get_by_id(return_id)
        )
        if not return_header:
            raise HTTPException(
                status_code=400,
                detail="Part Return not found",
            )
        issue_id = (
            return_header.issue_id
        )
        if quantity_returned <= 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Quantity Returned must be "
                    "greater than zero"
                ),
            )


        issue_details = (
            self.issue_detail_repository
            .get_all()
        )
        issued_qty = sum(
            float(
                item.quantity_issued or 0
            )
            for item in issue_details
            if item.issue_id == issue_id
            and item.part_id == part_id
        )
        if issued_qty == 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Part was not issued "
                    "under this Issue"
                ),
            )
        existing_return_qty = sum(
            float(
                item.quantity_returned or 0
            )
            for item in (
                self.repository.get_all()
            )
            if item.part_id == part_id
        )
        if (
            existing_return_qty
            + quantity_returned
        ) > issued_qty:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Quantity Returned cannot "
                    "exceed Quantity Issued"
                ),
            )
    def create(
        self,
        payload,
    ):

        self.validate_quantity_returned(
            payload.return_id,
            payload.part_id,
            payload.quantity_returned,
        )
        detail = (
            PartReturnDetail(
                return_id=
                payload.return_id,

                part_id=
                payload.part_id,

                quantity_returned=
                payload.quantity_returned,

                serial_number=
                payload.serial_number,

                remarks=
                payload.remarks,
            )
        )
        created_detail=(
            self.repository.create(
                detail
            )
        )
        ledger_service = (
            StockLedgerService(
                self.stock_ledger_repository
            )
        )
        ledger_service.record_return(
            part_id=payload.part_id,
            quantity=float(
                payload.quantity_returned
            ),
            reference_id=payload.return_id,
        )

        return created_detail

    def get_all(
        self,
    ):

        return (
            self.repository.get_all()
        )

    def get_by_id(
        self,
        return_detail_id: int,
    ):

        detail = (
            self.repository.get_by_id(
                return_detail_id
            )
        )

        if not detail:

            raise HTTPException(
                status_code=404,
                detail=
                "Part Return Detail not found",
            )

        return detail

    def update(
        self,
        return_detail_id: int,
        payload,
    ):

        detail = (
            self.get_by_id(
                return_detail_id
            )
        )
#        print(
#            f"return_id={detail.return_id}, "
#            f"part_id={detail.part_id}, "
#            f"qty={payload.quantity_returned}"
#        )
        if payload.quantity_returned is not None:
            self.validate_quantity_returned(
            detail.return_id,
            detail.part_id,
            float(payload.quantity_returned),
        )

        data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        for (
            key,
            value,
        ) in data.items():

            setattr(
                detail,
                key,
                value,
            )

        return (
            self.repository.update(
                detail
            )
        )

    def delete(
        self,
        return_detail_id: int,
    ):

        detail = (
            self.get_by_id(
                return_detail_id
            )
        )

        detail.active_flag = False

        return (
            self.repository.update(
                detail
            )
        )