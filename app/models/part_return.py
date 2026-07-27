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

from app.db.mixins import (
    AuditMixin,
    TimestampMixin,
)


class PartReturn(
    Base,
    AuditMixin,
    TimestampMixin,
):
    __tablename__ = "part_return"

    __table_args__ = {
        "schema": "transact"
    }

    return_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    return_number: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False,
    )

    issue_id: Mapped[int] = mapped_column(
        ForeignKey(
            "transact.part_issue.issue_id"
        )
    )

    return_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    returned_by_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        ),
        nullable=True,
    )

    received_by_employee_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        ),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )


class PartReturnDetail(
    Base,
    AuditMixin,
    TimestampMixin,
):
    __tablename__ = "part_return_detail"

    __table_args__ = {
        "schema": "transact"
    }

    return_detail_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    return_id: Mapped[int] = mapped_column(
        ForeignKey(
            "transact.part_return.return_id"
        )
    )

    part_id: Mapped[int] = mapped_column(
        ForeignKey(
            "inventory.part_master.part_id"
        )
    )

#    issue_id: Mapped[int] = mapped_column(
#        ForeignKey(
#            "transact.part_issue.issue_id"
#        )
#    )
    quantity_returned: Mapped[float] = mapped_column(
        Numeric(10, 2),
        default=0,
    )

    serial_number: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    remarks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
    )