from pydantic import BaseModel  #type: ignore


class PartReturnBase(BaseModel):

    issue_id: int

    returned_by_employee_id: int | None = None

    received_by_employee_id: int | None = None

    status: str = "OPEN"

    remarks: str | None = None


class PartReturnCreate(
    PartReturnBase
):
    pass


class PartReturnUpdate(
    BaseModel
):

    issue_id: int | None = None

    returned_by_employee_id: int | None = None

    received_by_employee_id: int | None = None

    status: str | None = None

    remarks: str | None = None

    active_flag: bool | None = None


class PartReturnResponse(
    PartReturnBase
):

    return_id: int

    return_number: str

    active_flag: bool

    model_config = {
        "from_attributes": True
    }