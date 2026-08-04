from datetime import datetime

from fastapi import HTTPException   #type:  ignore

from app.models.part_requisition import (
    PartRequisition,
)

from app.repositories.part_requisition_repository import (
    PartRequisitionRepository,
)


class PartRequisitionService:

    def __init__(
        self,
        repository:
        PartRequisitionRepository,
    ):
        self.repository = (
            repository
        )

    def _generate_number(
        self,
    ):

        year = (
            datetime.now().year
        )

        count = len(
            self.repository
            .get_all()
        ) + 1

        return (
            f"PR-"
            f"{year}-"
            f"{count:06d}"
        )

    def create(
        self,
        payload,
    ):

        requisition = (
            PartRequisition(
                requisition_number=
                self._generate_number(),

                vehicle_id=
                payload.vehicle_id,

                job_card_id=
                payload.job_card_id,

                technician_id=
                payload.technician_id,

                remarks=
                payload.remarks,

                status=
                payload.status,
            )
        )

        return (
            self.repository
            .create(
                requisition
            )
        )

    def get_all(
        self,
    ):
        return (
            self.repository
            .get_all()
        )

    def get_by_id(
        self,
        requisition_id: int,
    ):

        requisition = (
            self.repository
            .get_by_id(
                requisition_id
            )
        )

        if not requisition:

            raise HTTPException(
                status_code=404,
                detail=
                "Part Requisition not found",
            )

        return requisition

    def update(
        self,
        requisition_id,
        payload,
    ):

        requisition = (
            self.get_by_id(
                requisition_id
            )
        )

        data = (
            payload.model_dump(
                exclude_unset=True
            )
        )

        for key, value in (
            data.items()
        ):
            setattr(
                requisition,
                key,
                value,
            )

        return (
            self.repository
            .update(
                requisition
            )
        )

    def delete(
        self,
        requisition_id,
    ):

        requisition = (
            self.get_by_id(
                requisition_id
            )
        )

        requisition.active_flag = (
            False
        )

        return (
            self.repository
            .update(
                requisition
            )
        )
#submit for approval workflow
    def submit_request(
        self,
        request_id: int,
    ):

        request = (
            self.repository
            .get_by_id(request_id)
        )

        if not request:

            raise HTTPException(
                status_code=404,
                detail="Request not found",
            )

        if (
            request.status
            != "DRAFT"
        ):

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only DRAFT requests can be submitted"
                ),
            )

        request.status = (
            "SUBMITTED"
        )

        return (
            self.repository.update(
                request
            )
        )
#Approval request
    def approve_request(
        self,
        request_id: int,
    ):

        request = (
            self.repository
            .get_by_id(request_id)
        )

        if not request:

            raise HTTPException(
                status_code=404,
                detail="Request not found",
            )

        if (
            request.status!= "OPEN" 
        ):

            raise HTTPException(
                status_code=400,
                detail=
                "Request must be submitted first",
            )
        request.status = ("APPROVED")
        request.approved_by = 3
        request.approved_at = (datetime.utcnow())

        return (
            self.repository.update(
                request
            )
        )
