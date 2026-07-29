from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Numeric,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.db.base import Base

from app.db.mixins import (
    AuditMixin,
    TimestampMixin,
)


class OpeningStock(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "opening_stock"

    __table_args__ = {
        "schema": "inventory",
    }

    opening_stock_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    part_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.part_master.part_id"
        )
    )

    opening_quantity: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    effective_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )