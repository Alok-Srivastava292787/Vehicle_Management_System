import pytest

from app.db.session import SessionLocal
from app.models.master import VehicleMaster, EmployeeMaster
from app.models.master import DriverMaster

import uuid
import app.models

@pytest.fixture
def vehicle(db):

    vehicle = VehicleMaster(
        rc_number=f"TEST-{uuid.uuid4()}",
        engine_no=f"ENG-{uuid.uuid4()}",
        chassis_no=f"CH-{uuid.uuid4()}"
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    return vehicle


@pytest.fixture
def driver(db):

    driver = DriverMaster(
        driver_name="Driver",
        mobile_number="9999999999"
    )

    db.add(driver)
    db.commit()

    return driver

@pytest.fixture
def employee(db):

    employee = EmployeeMaster(
        full_name="John",
        phone_number="9999999999"
    )

    db.add(employee)
    db.commit()

    return employee


@pytest.fixture
def db():

    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
