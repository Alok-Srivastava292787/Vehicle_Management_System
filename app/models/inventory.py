
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class PartMaster(Base):

    __tablename__ = "part_master"
    __table_args__ = {"schema": "inventory"}

    part_id: Mapped[int] = mapped_column(primary_key=True)

    part_code: Mapped[str | None] = mapped_column(
        String(100)
    )

    part_name: Mapped[str | None] = mapped_column(
        String(300)
    )


class PartRequest(Base):

    __tablename__ = "part_request"
    __table_args__ = {"schema": "inventory"}

    request_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    request_number: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.vehicle_master.vehicle_id"
        ),nullable=False
    )


class StockTransaction(Base):

    __tablename__ = "stock_transaction"
    __table_args__ = {"schema": "inventory"}

    stock_txn_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    part_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.part_master.part_id"
        )
    )

    reference_id: Mapped[int] = mapped_column()
