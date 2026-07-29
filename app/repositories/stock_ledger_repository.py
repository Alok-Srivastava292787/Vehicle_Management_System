from sqlalchemy.orm import Session

from app.models.stock_ledger import (
    StockLedger,
)


class StockLedgerRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        item,
    ):

        self.db.add(item)

        self.db.commit()

        self.db.refresh(item)

        return item

    def get_by_id(
        self,
        ledger_id: int,
    ):

        return (
            self.db.query(
                StockLedger
            )
            .filter(
                StockLedger.ledger_id
                == ledger_id
            )
            .first()
        )

    def get_all(
        self,
    ):

        return (
            self.db.query(
                StockLedger
            )
            .order_by(
                StockLedger.ledger_id.desc()
            )
            .all()
        )

    def update(
        self,
        item,
    ):

        self.db.commit()

        self.db.refresh(item)

        return item

    def get_latest_balance(
        self,
        part_id: int,
    ):

        row = (
            self.db.query(
                StockLedger
            )
            .filter(
                StockLedger.part_id
                == part_id
            )
            .order_by(
                StockLedger.ledger_id.desc()
            )
            .first()
        )

        if not row:

            return 0

        return float(
            row.balance_quantity
        )
    def get_latest_balances(
    self,
):

        rows = (
            self.db.query(
                StockLedger
            )
            .order_by(
                StockLedger.part_id,
                StockLedger.ledger_id.desc(),
            )
            .all()
        )

        latest = {}

        for row in rows:

            if (
                row.part_id
                not in latest
            ):
                latest[
                    row.part_id
                ] = row

        return list(
            latest.values()
        )
