from pydantic import BaseModel  #type: ignore


class PartIssueBase(
    BaseModel
):
    requisition_id: int

    issued_by_employee_id: int | None = None

    received_by_employee_id: int | None = None

    status: str = "OPEN"

    remarks: str | None = None


class PartIssueCreate(
    PartIssueBase
):
    pass


class PartIssueUpdate(
    BaseModel
):

    requisition_id: int | None = None

    issued_by_employee_id: int | None = None

    received_by_employee_id: int | None = None

    status: str | None = None

    remarks: str | None = None

    active_flag: bool | None = None


class PartIssueResponse(
    PartIssueBase
):

    issue_id: int

    issue_number: str

    active_flag: bool

    model_config = {
        "from_attributes": True,
    }