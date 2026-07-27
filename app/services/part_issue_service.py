from datetime import datetime

from fastapi import (    HTTPException,)    #type: ignore

from app.models.part_issue import (
    PartIssue,
)

from app.repositories.part_issue_repository import (
    PartIssueRepository,
)


class PartIssueService:

    def __init__(
        self,
        repository:
        PartIssueRepository,
    ):
        self.repository = repository

    def generate_issue_number(
        self,
    ):

        current_year = (
            datetime.now().year
        )

        latest_issue = (
            self.repository.get_all()
        )

        sequence = (
            len(
                latest_issue
            ) + 1
        )

        return (
            f"PI-{current_year}-"
            f"{sequence:06d}"
        )

    def create(
        self,
        payload,
    ):

        issue = (
            PartIssue(
                issue_number=
                self.generate_issue_number(),

                requisition_id=
                payload.requisition_id,

                issued_by_employee_id=
                payload.issued_by_employee_id,

                received_by_employee_id=
                payload.received_by_employee_id,

                status=
                payload.status,

                remarks=
                payload.remarks,
            )
        )

        return self.repository.create(
            issue
        )

    def get_all(
        self,
    ):

        return (
            self.repository.get_all()
        )

    def get_by_id(
        self,
        issue_id: int,
    ):

        issue = (
            self.repository.get_by_id(
                issue_id
            )
        )

        if not issue:

            raise HTTPException(
                status_code=404,
                detail=
                "Part Issue not found",
            )

        return issue

    def update(
        self,
        issue_id: int,
        payload,
    ):

        issue = (
            self.get_by_id(
                issue_id
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
                issue,
                key,
                value,
            )

        return (
            self.repository.update(
                issue
            )
        )

    def delete(
        self,
        issue_id: int,
    ):

        issue = (
            self.get_by_id(
                issue_id
            )
        )

        issue.active_flag = False

        return (
            self.repository.update(
                issue
            )
        )