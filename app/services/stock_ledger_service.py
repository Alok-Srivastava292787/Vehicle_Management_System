from fastapi import HTTPException   #type: ignore
from collections import defaultdict
from app.models.stock_ledger import (
    StockLedger,
)

from app.repositories.stock_ledger_repository import (
    StockLedgerRepository,
)
from app.repositories.part_repository import (
    PartRepository,
)

class StockLedgerService:
    def __init__(
        self,
        repository:
        StockLedgerRepository,

        part_repository:
        PartRepository,
    ):

        self.repository = repository

        self.part_repository = (
            part_repository
        )
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
    def get_inventory_summary(
    self,
):
        records = (
            self.repository.get_all()
        )
        total_stock = sum(
            float(
                x.balance_quantity
                or 0
            )
            for x in records
        )

        total_issued = sum(
            float(
                x.quantity_out
                or 0
            )
            for x in records
        )

        total_returned = sum(
            float(
                x.quantity_in
                or 0
            )
            for x in records
            if (
                x.transaction_type
                == "RETURN"
            )
        )

        return {

            "total_stock":
            total_stock,

            "total_issued":
            total_issued,

            "total_returned":
            total_returned,

            "total_transactions":
            len(records),
        }
    def get_low_stock_parts(
    self,
):
        records = (
            self.repository.get_all()
        )
        low_stock_parts = [
            {
                "part_id": x.part_id,
                "balance_quantity": x.balance_quantity,
            }
            for x in records
            if (
                x.balance_quantity
                < 10
            )
        ]
        return low_stock_parts
    def get_low_stock_parts(
        self,
    ):

        balances = (
            self.repository
            .get_latest_balances()
        )

        results = []

        for row in balances:

            part = (
                self.part_repository
                .get_by_id(
                    row.part_id
                )
            )

            if not part:

                continue

            minimum_stock = (
                float(
                    part.minimum_stock_qty
                    or 0
                )
            )

            current_balance = (
                float(
                    row.balance_quantity
                    or 0
                )
            )

            if (
                current_balance
                <= minimum_stock
            ):

                results.append(
                    {
                        "part_id":
                        part.part_id,

                        "part_name":
                        part.part_name,

                        "balance":
                        current_balance,

                        "minimum_stock_qty":
                        minimum_stock,
                    }
                )

        return results
    def get_top_consumed_parts(
    self,
):

        ledger_rows = (
            self.repository.get_all()
        )

        consumption = defaultdict(float)

        for row in ledger_rows:

            if (
                row.transaction_type
                == "ISSUE"
            ):

                consumption[
                    row.part_id
                ] += float(
                    row.quantity_out
                    or 0
                )

        results = []

        for (
            part_id,
            qty,
        ) in consumption.items():

            part = (
                self.part_repository
                .get_by_id(
                    part_id
                )
            )

            if not part:

                continue

            results.append(
                {
                    "part_id":
                    part_id,

                    "part_name":
                    part.part_name,

                    "quantity_consumed":
                    qty,
                }
            )

        results.sort(
            key=lambda x:
            x[
                "quantity_consumed"
            ],
            reverse=True,
        )

        return results[:10]
#Top returned parts
    def get_top_returned_parts(
    self,
):

        ledger_rows = (
            self.repository.get_all()
        )

        returned = defaultdict(float)

        for row in ledger_rows:

            if (
                row.transaction_type
                == "RETURN"
            ):

                returned[
                    row.part_id
                ] += float(
                    row.quantity_in
                    or 0
                )

        results = []

        for (
            part_id,
            qty,
        ) in returned.items():

            part = (
                self.part_repository
                .get_by_id(
                    part_id
                )
            )

            if not part:

                continue

            results.append(
                {
                    "part_id":
                    part_id,

                    "part_name":
                    part.part_name,

                    "quantity_returned":
                    qty,
                }
            )

        results.sort(
            key=lambda x:
            x["quantity_returned"],
            reverse=True,
        )
        return results[:10]
    def get_issue_return_trend(
    self,
):

        rows = (
            self.repository.get_all()
        )

        trend = defaultdict(
            lambda: {
                "issue": 0,
                "return": 0,
            }
        )

        for row in rows:

            if (
                not row.transaction_date
            ):
                continue

            month = (
                row.transaction_date
                .strftime("%Y-%m")
            )

            if (
                row.transaction_type
                == "ISSUE"
            ):

                trend[month][
                    "issue"
                ] += float(
                    row.quantity_out
                    or 0
                )

            if (
                row.transaction_type
                == "RETURN"
            ):

                trend[month][
                    "return"
                ] += float(
                    row.quantity_in
                    or 0
                )

        results = []

        for (
            month,
            values,
        ) in sorted(
            trend.items()
        ):

            results.append(
                {
                    "month":
                    month,

                    "issue":
                    values[
                        "issue"
                    ],

                    "return":
                    values[
                        "return"
                    ],
                }
            )

        return results
