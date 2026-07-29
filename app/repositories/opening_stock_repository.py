from sqlalchemy.orm import Session

from app.models.opening_stock import (
    OpeningStock,
)


class OpeningStockRepository:

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
        opening_stock_id: int,
    ):

        return (
            self.db.query(
                OpeningStock
            )
            .filter(
                OpeningStock.opening_stock_id
                == opening_stock_id
            )
            .first()
        )

    def get_all(
        self,
    ):

        return (
            self.db.query(
                OpeningStock
            )
            .order_by(
                OpeningStock.opening_stock_id.desc()
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

    def get_active_by_part(
        self,
        part_id: int,
    ):

        return (
            self.db.query(
                OpeningStock
            )
            .filter(
                OpeningStock.part_id
                == part_id,
                OpeningStock.active_flag.is_(True),
            )
            .first()
        )