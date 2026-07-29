from pydantic import BaseModel  #type: ignore


class OpeningStockBase(
    BaseModel
):

    part_id: int

    opening_quantity: float

    remarks: str | None = None


class OpeningStockCreate(
    OpeningStockBase
):
    pass


class OpeningStockUpdate(
    BaseModel
):

    opening_quantity: float | None = None

    remarks: str | None = None

    active_flag: bool | None = None


class OpeningStockResponse(
    OpeningStockBase
):

    opening_stock_id: int

    active_flag: bool

    model_config = {
        "from_attributes": True
    }