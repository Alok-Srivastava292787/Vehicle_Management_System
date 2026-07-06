import uuid

from app.models.master import DriverMaster
from app.models.master import VehicleMaster

from app.models.maintenance import (
    VehicleComplaint
)

from app.repositories.complaint_repository import (
    ComplaintRepository,
)


def test_get_complaint_by_vehicle(db):

    vehicle = VehicleMaster(
        rc_number=f"TS-{uuid.uuid4()}"
    )

    driver = DriverMaster(
        driver_name="Driver",
        mobile_number="8888888888"
    )

    db.add(vehicle)
    db.add(driver)

    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery Issue"
    )

    repo = ComplaintRepository(db)

    repo.create(complaint)

    result = repo.get_by_vehicle(
        vehicle.vehicle_id
    )

    assert len(result) == 1