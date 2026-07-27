from sqlalchemy.orm import Session

from app.models.part_return import (
    PartReturn,
)


class PartReturnRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    def create(
        self,
        item: PartReturn,
    ):

        self.db.add(item)

        self.db.commit()

        self.db.refresh(item)

        return item

    def get_by_id(
        self,
        return_id: int,
    ):

        return (
            self.db.query(
                PartReturn
            )
            .filter(
                PartReturn.return_id
                == return_id
            )
            .first()
        )

    def get_all(
        self,
    ):
        return (
            self.db.query(
                PartReturn
            )
            .order_by(
                PartReturn.return_id.desc()
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
