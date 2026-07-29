from fastapi import HTTPException   #type: ignore

from app.models.stock_ledger import (
    StockLedger,
)

from app.repositories.stock_ledger_repository import (
    StockLedgerRepository,
)


class StockLedgerService:
    def __init__(
        self,
        repository:
        StockLedgerRepository,
    ):
        self.repository = repository

    def create(
        self,
        payload,
    ):

        item = StockLedger(
            part_id=
            payload.part_id,
            transaction_type=
            payload.transaction_type,
            reference_id=
            payload.reference_id,
            quantity_in=
            payload.quantity_in,
            quantity_out=
            payload.quantity_out,
            balance_quantity=
            payload.balance_quantity,
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
        ledger_id: int,
    ):
        item = (
            self.repository
            .get_by_id(
                ledger_id
            )
        )
        if not item:
            raise HTTPException(
                status_code=404,
                detail=
                "Stock Ledger not found",
            )
        return item

    def update(
        self,
        ledger_id: int,
        payload,
    ):
        item = (
            self.get_by_id(
                ledger_id
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
        ledger_id: int,
    ):
        item = (
            self.get_by_id(
                ledger_id
            )
        )
        item.active_flag = False
        return (
            self.repository.update(
                item
            )
        )

    def get_balance(
        self,
        part_id: int,
    ):
        return {

            "part_id":
            part_id,

            "balance":
            self.repository
            .get_latest_balance(
                part_id
            ),
        }
    
    def record_issue(
    self,
    part_id: int,
    quantity: float,
    reference_id: int,
    ):
        latest_balance = (
            self.repository
            .get_latest_balance(
                part_id
            )
        )
        new_balance = (
            latest_balance
            - quantity
        )
        item = StockLedger(
            part_id=part_id,
            transaction_type=
            "ISSUE",
            reference_id=
            reference_id,
            quantity_in=0,
            quantity_out=
            quantity,
            balance_quantity=
            new_balance,
        )
        return (
            self.repository.create(
                item
            )
        )

    def record_return(
    self,
    part_id: int,
    quantity: float,
    reference_id: int,
    ):

        latest_balance = (
            self.repository
            .get_latest_balance(
                part_id
            )
        )

        new_balance = (
            latest_balance
            + quantity
        )

        item = StockLedger(
            part_id=part_id,

            transaction_type=
            "RETURN",

            reference_id=
            reference_id,

            quantity_in=
            quantity,

            quantity_out=0,

            balance_quantity=
            new_balance,
        )

        return (
            self.repository.create(
                item
            )
        )
