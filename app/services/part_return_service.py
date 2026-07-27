from datetime import datetime

from fastapi import HTTPException   #type: ignore

from app.models.part_return import (
    PartReturn,
)

from app.repositories.part_return_repository import (
    PartReturnRepository,
)


class PartReturnService:

    def __init__(
        self,
        repository:
        PartReturnRepository,
    ):
        self.repository = repository

    def generate_return_number(
        self,
    ):

        year = (
            datetime.now().year
        )

        count = len(
            self.repository.get_all()
        ) + 1

        return (
            f"PRT-{year}-"
            f"{count:06d}"
        )

    def create(
        self,
        payload,
    ):

        item = PartReturn(
#            return_id=payload.return_id,

            return_number=
            self.generate_return_number(),

            issue_id=
            payload.issue_id,

            returned_by_employee_id=
            payload.returned_by_employee_id,

            received_by_employee_id=
            payload.received_by_employee_id,

            status=
            payload.status,

            remarks=
            payload.remarks,
        )

        return (
            self.repository.create(
                item
            )
        )

    def get_all(
        self,
    ):
        return (
            self.repository.get_all()
        )

    def get_by_id(
        self,
        return_id: int,
    ):

        item = (
            self.repository.get_by_id(
                return_id
            )
        )

        if not item:

            raise HTTPException(
                status_code=404,
                detail=
                "Part Return not found",
            )

        return item

    def update(
        self,
        return_id: int,
        payload,
    ):

        item = (
            self.get_by_id(
                return_id
            )
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
                item,
                key,
                value,
            )

        return (
            self.repository.update(
                item
            )
        )

    def delete(
        self,
        return_id: int,
    ):

        item = (
            self.get_by_id(
                return_id
            )
        )

        item.active_flag = False

        return (
            self.repository.update(
                item
            )
        )