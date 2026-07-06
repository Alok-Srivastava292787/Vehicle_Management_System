import uuid

from app.models.master import (
    DriverMaster,
    VehicleMaster,
)

from app.repositories.complaint_repository import (
    ComplaintRepository,
)

from app.repositories.driver_repository import (
    DriverRepository,
)

from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.schemas.complaint import (
    ComplaintCreate,
)

from app.services.complaint_service import (
    ComplaintService,
)


def test_create_complaint_service(
    db
):

    vehicle = VehicleMaster(
        rc_number=f"TS-{uuid.uuid4()}"
    )

    driver = DriverMaster(
        driver_name="Driver",
        mobile_number="9999999999",
        dl_number=f"DL-{uuid.uuid4()}",
    )

    db.add(vehicle)
    db.add(driver)

    db.commit()

    service = ComplaintService(
        ComplaintRepository(db),
        VehicleRepository(db),
        DriverRepository(db),
    )

    payload = ComplaintCreate(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery Problem",
    )

    complaint = (
        service.create_complaint(
            payload
        )
    )

    assert complaint.complaint_id