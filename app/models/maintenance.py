
from sqlalchemy import ForeignKey
from sqlalchemy import Text, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base
from app.db.mixins import AuditMixin
from app.db.mixins import TimestampMixin


class VehicleComplaint(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "vehicle_complaint"
    __table_args__ = {"schema": "maintenance"}

    complaint_id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("master.vehicle_master.vehicle_id")
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("master.driver_master.driver_id")
    )

    issue_description: Mapped[str | None] = mapped_column(Text)

    vehicle = relationship(
        "VehicleMaster",
        back_populates="complaints"
    )



class TechnicianInspection(
    Base,
    AuditMixin,
    TimestampMixin,
):
    __tablename__ = "technician_inspection"
    __table_args__ = {"schema": "maintenance"}

    inspection_id: Mapped[int] = mapped_column(
        primary_key=True
    )

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey(
            "maintenance.vehicle_complaint.complaint_id"
        )
    )

    technician_id: Mapped[int] = mapped_column(
        ForeignKey(
            "master.employee_master.employee_id"
        )
    )

    observed_issue: Mapped[str | None] = mapped_column(Text)

    operator_notes: Mapped[str | None] = mapped_column(Text)

    status: Mapped[str | None] = mapped_column(String(30))


class MaintenanceJobCard(
    Base,
    AuditMixin,
    TimestampMixin,
):

    __tablename__ = "maintenance_job_card"
    __table_args__ = {"schema": "transact"}

    job_card_id: Mapped[int] = mapped_column(primary_key=True)

    complaint_id: Mapped[int] = mapped_column(
        ForeignKey(
            "maintenance.vehicle_complaint.complaint_id"
        )
    )

    inspection_id: Mapped[int] = mapped_column(
        ForeignKey(
            "maintenance.technician_inspection.inspection_id"
        )
    )