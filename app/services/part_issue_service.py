from datetime import datetime

from fastapi import (    HTTPException,)    #type: ignore

from app.models.part_issue import (
    PartIssue,
    PartIssueDetail
)

from app.repositories.part_issue_repository import (    PartIssueRepository,)
from app.repositories.part_requisition_repository import (  PartRequisitionRepository)
from app.repositories.part_requisition_repository import (  PartRequisitionRepository,)

from app.repositories.part_requisition_detail_repository import (PartRequisitionDetailRepository,)

from app.repositories.part_issue_detail_repository import (PartIssueDetailRepository,)

class PartIssueService:

    def __init__(
        self,
        repository: PartIssueRepository,
        requisition_repository: PartRequisitionRepository,
        requisition_detail_repository: PartRequisitionDetailRepository,
        issue_detail_repository: PartIssueDetailRepository,
    ):

        self.repository = repository
        self.requisition_repository = (requisition_repository)
        self.requisition_detail_repository = (requisition_detail_repository)
        self.issue_detail_repository = (issue_detail_repository)

    
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
        requisition = (self.requisition_repository.get_by_id( payload.requisition_id)        )
        if not requisition:
            raise HTTPException(
                status_code=404,
                detail="Requisition not found",
            )
        if ( requisition.status!= "APPROVED"):
            raise HTTPException(
                status_code=400,
                detail=
                "Only APPROVED requisitions can be issued",
            )
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
        issue = (self.repository.create(issue))
        requisition = (self.requisition_repository.get_by_id(payload.requisition_id))
        if (requisition.status== "APPROVED"):
            requisition.status = ("ISSUED")
            self.requisition_repository.update(requisition)

        return issue
        

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

    def create_from_requisition(
        self,
        requisition_id: int,
    ):
        requisition = (self.requisition_repository.get_by_id(requisition_id))
        if not requisition:
            raise HTTPException(
                status_code=404,
                detail=
                "Requisition not found",
            )
        if (
            requisition.status
            != "APPROVED"
        ):
            raise HTTPException(
                status_code=400,
                detail=
                "Only APPROVED requisitions can create issues",
            )
        issue = (
            PartIssue(
                issue_number=self.generate_issue_number(),
                requisition_id=requisition.requisition_id,
                issued_by_employee_id=4,
                received_by_employee_id=requisition.technician_id,
                status="OPEN",
                remarks=
                    f"Generated from "
                    f"Requisition "
                    f"{requisition.requisition_number}",
                )
        )
        issue = (self.repository.create(issue))
        requisition_details = (self.requisition_detail_repository.get_by_requisition_id(requisition_id))
        for item in requisition_details:
            issue_detail = (
                PartIssueDetail(
                    issue_id=issue.issue_id,
                    part_id=item.part_id,
                    quantity_issued=item.quantity_required,
                    active_flag=True,
                    remarks=(
                            f"Generated from "
                            f"Requisition "
                            f"{requisition.requisition_number}"
                            )
                )
            )
            self.issue_detail_repository.create(
                issue_detail
            )
        requisition.status = (
            "ISSUE_CREATED"
        )
        requisition.issue_id = issue.issue_id
        self.requisition_repository.update(
            requisition
        )
        return {
            "issue_id": issue.issue_id,
            "issue_number": issue.issue_number,
            "requisition_id":requisition.requisition_id,
        }