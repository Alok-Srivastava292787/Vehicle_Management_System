from pydantic import BaseModel  #type: ignore


class PartReturnDetailBase(
    BaseModel
):
    return_id: int

    part_id: int

    quantity_returned: float = 0

    serial_number: str | None = None

    remarks: str | None = None


class PartReturnDetailCreate(
    PartReturnDetailBase
):
    pass


class PartReturnDetailUpdate(
    BaseModel
):

    return_id: int | None = None

    part_id: int | None = None

#    issue_id: int | None = None


    quantity_returned: float | None = None

    serial_number: str | None = None

    remarks: str | None = None

    active_flag: bool | None = None


class PartReturnDetailResponse(
    PartReturnDetailBase
):

    return_detail_id: int

    active_flag: bool

    model_config = {
        "from_attributes": True
    }