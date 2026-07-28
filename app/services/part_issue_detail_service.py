from fastapi import (    HTTPException,)    #type: ignore

from app.repositories.part_issue_repository import (
    PartIssueRepository,
)

from app.repositories.part_requisition_detail_repository import (
    PartRequisitionDetailRepository,
)
from app.models.part_issue import (
    PartIssueDetail,
)

from app.repositories.part_issue_detail_repository import (
    PartIssueDetailRepository,
)


class PartIssueDetailService:

    def __init__(
        self,
        repository:
        PartIssueDetailRepository,

        issue_repository:
        PartIssueRepository,

        requisition_detail_repository:
        PartRequisitionDetailRepository,
    ):

        self.repository = repository

        self.issue_repository = (
            issue_repository
        )

        self.requisition_detail_repository = (
            requisition_detail_repository
        )
    def validate_issue_quantity(
        self,
        issue_id: int,
        part_id: int,
        quantity_issued: float,
    ):
        if quantity_issued <= 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Quantity Issued must be "
                    "greater than zero"
                ),
            )

        issue_header = (
            self.issue_repository
            .get_by_id(issue_id)
        )

        if not issue_header:

            raise HTTPException(
                status_code=400,
                detail="Part Issue not found",
            )

        requisition_id = (
            issue_header.requisition_id
        )

        requisition_details = (
            self.requisition_detail_repository
            .get_all()
        )

        requested_qty = sum(
            float(
                item.quantity_required or 0
            )
            for item in requisition_details
            if (
                item.requisition_id
                == requisition_id
                and
                item.part_id
                == part_id
                and
                item.active_flag
            )
        )

        if requested_qty <= 0:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Part not found in "
                    "Requisition"
                ),
            )

        existing_issued_qty = sum(
            float(
                item.quantity_issued or 0
            )
            for item in (
                self.repository.get_all()
            )
            if (
                item.issue_id
                == issue_id
                and
                item.part_id
                == part_id
                and
                item.active_flag
            )
        )

        if (
            existing_issued_qty
            + quantity_issued
        ) > requested_qty:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Issued Quantity cannot "
                    "exceed Requested Quantity"
                ),
            )
    def create(
        self,
        payload,
    ):
        self.validate_issue_quantity(
            payload.issue_id,
            payload.part_id,
            float(
                payload.quantity_issued
                or 0
            ),
        )
        detail = (
            PartIssueDetail(
                issue_id=
                payload.issue_id,

                part_id=
                payload.part_id,

                quantity_issued=
                payload.quantity_issued,

                serial_number=
                payload.serial_number,

                remarks=
                payload.remarks,
            )
        )

        return self.repository.create(
            detail
        )

    def get_all(
        self,
    ):
        return (
            self.repository.get_all()
        )

    def get_by_id(
        self,
        issue_detail_id: int,
    ):
        detail = (
            self.repository.get_by_id(
                issue_detail_id
            )
        )

        if not detail:
            raise HTTPException(
                status_code=404,
                detail=
                "Part Issue Detail not found",
            )

        return detail

    def update(
        self,
        issue_detail_id: int,
        payload,
    ):
        detail = (
            self.get_by_id(
                issue_detail_id
            )
        )

        quantity_to_validate = (
            payload.quantity_issued
            if payload.quantity_issued is not None
            else detail.quantity_issued
        )

        part_id_to_validate = (
            payload.part_id
            if payload.part_id is not None
            else detail.part_id
        )

        self.validate_issue_quantity(
            detail.issue_id,
            part_id_to_validate,
            float(
                quantity_to_validate
                or 0
            ),
        )

        data = payload.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():
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
        issue_detail_id: int,
    ):
        detail = (
            self.get_by_id(
                issue_detail_id
            )
        )

        detail.active_flag = False

        return (
            self.repository.update(
                detail
            )
        )