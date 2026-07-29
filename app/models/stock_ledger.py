from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base

from app.db.mixins import (AuditMixin,TimestampMixin,) 


class StockLedger(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "stock_ledger"

    __table_args__ = {
        "schema": "inventory"
    }

    ledger_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    part_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.part_master.part_id"
        )
    )

    transaction_type: Mapped[str] = mapped_column(
        String(20)
    )

    reference_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    transaction_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    quantity_in: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    quantity_out: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    balance_quantity: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )