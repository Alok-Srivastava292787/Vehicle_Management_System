import uuid

from app.models.master import (
    DriverMaster,
    EmployeeMaster,
    VehicleMaster,
)

from app.models.maintenance import (
    TechnicianInspection,
    VehicleComplaint,
)

from app.repositories.inspection_repository import (
    InspectionRepository,
)


def test_get_inspection_by_id(
    db,
):

    vehicle = VehicleMaster(
        rc_number=f"TS-{uuid.uuid4()}",
    )

    driver = DriverMaster(
        driver_name="Driver",
        mobile_number="9999999999",
    )

    technician = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="Tech User",
        phone_number="8888888888",
    )

    db.add_all(
        [
            vehicle,
            driver,
            technician,
        ]
    )

    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery Issue",
    )

    db.add(complaint)

    db.commit()

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=technician.employee_id,
        observed_issue="Battery Dead",
    )

    db.add(inspection)

    db.commit()

    repo = InspectionRepository(
        db
    )

    result = repo.get_by_id(
        inspection.inspection_id
    )

    assert result is not None

    assert (
        result.inspection_id
        == inspection.inspection_id
    )