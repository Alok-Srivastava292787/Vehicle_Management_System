from pydantic import BaseModel  #type: ignore


class StockLedgerBase(
    BaseModel
):

    part_id: int

    transaction_type: str

    reference_id: int | None = None

    quantity_in: float = 0

    quantity_out: float = 0

    balance_quantity: float = 0

    remarks: str | None = None


class StockLedgerCreate(
    StockLedgerBase
):
    pass


class StockLedgerUpdate(
    BaseModel
):

    remarks: str | None = None

    active_flag: bool | None = None


class StockLedgerResponse(
    StockLedgerBase
):

    ledger_id: int

    active_flag: bool

    model_config = {
        "from_attributes": True
    }