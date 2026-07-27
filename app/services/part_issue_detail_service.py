from fastapi import (    HTTPException,)    #type: ignore

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
    ):
        self.repository = repository

    def create(
        self,
        payload,
    ):
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