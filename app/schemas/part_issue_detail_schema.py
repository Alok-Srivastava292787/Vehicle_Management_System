from pydantic import BaseModel  #type: ignore


class PartIssueDetailBase(
    BaseModel
):
    issue_id: int

    part_id: int

    quantity_issued: float = 0

    serial_number: str | None = None

    remarks: str | None = None


class PartIssueDetailCreate(
    PartIssueDetailBase
):
    pass


class PartIssueDetailUpdate(
    BaseModel
):
    issue_id: int | None = None

    part_id: int | None = None

    quantity_issued: float | None = None

    serial_number: str | None = None

    remarks: str | None = None

    active_flag: bool | None = None


class PartIssueDetailResponse(
    PartIssueDetailBase
):
    issue_detail_id: int

    active_flag: bool

    model_config = {
        "from_attributes": True,
    }