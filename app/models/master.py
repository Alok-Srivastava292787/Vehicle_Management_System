from datetime import date

from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base import Base


class EmployeeMaster(Base):

    __tablename__ = "employee_master"
    __table_args__ = {"schema": "master"}

    employee_id: Mapped[int] = mapped_column(primary_key=True)

    employee_type: Mapped[str | None] = mapped_column(String(30))

    full_name: Mapped[str | None] = mapped_column(String(100))

    phone_number: Mapped[str] = mapped_column(String(15))
    
    inspections = relationship(
        "TechnicianInspection",
        back_populates="technician"
    )


class DriverMaster(Base):

    __tablename__ = "driver_master"
    __table_args__ = {"schema": "master"}

    driver_id: Mapped[int] = mapped_column(primary_key=True)

    driver_name: Mapped[str] = mapped_column(String(200))

    mobile_number: Mapped[str] = mapped_column(String(20))

    dl_number: Mapped[str | None] = mapped_column(
        String(100),
        unique=True
    )

    dl_expiry_date: Mapped[date | None] = mapped_column(Date)


class VehicleMaster(Base):

    __tablename__ = "vehicle_master"
    __table_args__ = {"schema": "master"}

    vehicle_id: Mapped[int] = mapped_column(primary_key=True)

    vehicle_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "reference.vehicle_type_ref.vehicle_type_id"
        )
    )

    fuel_type_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "reference.fuel_type_ref.fuel_type_id"
        )
    )

    rc_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    engine_no: Mapped[str | None] = mapped_column(
        String(100),
        unique=True
    )

    chassis_no: Mapped[str | None] = mapped_column(
        String(100),
        unique=True
    )

    purchase_date: Mapped[date | None] = mapped_column(Date)

    fuel_capacity: Mapped[float | None] = mapped_column(
        Numeric(4, 2)
    )

    active_flag: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    complaints = relationship(
        "VehicleComplaint",
        back_populates="vehicle"
    )
    
    job_cards = relationship(
        "MaintenanceJobCard",
        back_populates="vehicle"
    )
    pm_checklists = relationship(
        "PreventiveMaintenanceChecklist",
        back_populates="vehicle"
    )

