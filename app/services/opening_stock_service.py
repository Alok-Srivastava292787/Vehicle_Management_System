from fastapi import (HTTPException,)    #type: ignore

from app.models.opening_stock import (
    OpeningStock,
)

from app.models.stock_ledger import (
    StockLedger,
)

from app.repositories.opening_stock_repository import (
    OpeningStockRepository,
)

from app.repositories.stock_ledger_repository import (
    StockLedgerRepository,
)


class OpeningStockService:

    def __init__(
        self,
        repository:
        OpeningStockRepository,

        stock_ledger_repository:
        StockLedgerRepository,
    ):

        self.repository = repository

        self.stock_ledger_repository = (
            stock_ledger_repository
        )

    def create(
        self,
        payload,
    ):

        existing = (
            self.repository
            .get_active_by_part(
                payload.part_id
            )
        )

        if existing:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Opening Stock already exists "
                    "for this Part"
                ),
            )

        item = OpeningStock(
            part_id=
            payload.part_id,

            opening_quantity=
            payload.opening_quantity,

            remarks=
            payload.remarks,
        )

        created = (
            self.repository.create(
                item
            )
        )

        ledger = StockLedger(
            part_id=payload.part_id,
            transaction_type= "OPENING",
            reference_id= created.opening_stock_id,
            quantity_in=  payload.opening_quantity,
            quantity_out=0,
            balance_quantity= payload.opening_quantity,
            remarks=  payload.remarks,
        )

        self.stock_ledger_repository.create(
            ledger
        )
#        print(f"from service:{created}")
#        print(f"opening stock id: {created.opening_stock_id}")
        return created

    def get_all(
        self,
    ):
        return (
            self.repository.get_all()
        )

    def get_by_id(
        self,
        opening_stock_id: int,
    ):

        item = (
            self.repository
            .get_by_id(
                opening_stock_id
            )
        )

        if not item:

            raise HTTPException(
                status_code=404,
                detail=
                "Opening Stock not found",
            )

        return item

    def update(
        self,
        opening_stock_id: int,
        payload,
    ):

        item = (
            self.get_by_id(
                opening_stock_id
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
        opening_stock_id: int,
    ):

        item = (
            self.get_by_id(
                opening_stock_id
            )
        )

        item.active_flag = False

        return (
            self.repository.update(
                item
            )
        )