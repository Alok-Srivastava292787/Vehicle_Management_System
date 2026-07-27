from sqlalchemy.orm import Session

from app.models.part_return import (
    PartReturnDetail,
)


class PartReturnDetailRepository:

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
        return_detail_id: int,
    ):

        return (
            self.db.query(
                PartReturnDetail
            )
            .filter(
                PartReturnDetail.return_detail_id
                == return_detail_id
            )
            .first()
        )

    def get_all(
        self,
    ):
        return (
            self.db.query(
                PartReturnDetail
            )
            .order_by(
                PartReturnDetail.return_detail_id.desc()
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