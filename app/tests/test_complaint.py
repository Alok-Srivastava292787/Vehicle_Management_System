from app.models.maintenance import VehicleComplaint
from app.models.master import DriverMaster
from app.models.master import VehicleMaster


def test_create_complaint(db):

    vehicle = VehicleMaster(
        rc_number="KA01AA0002"
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
        issue_description="Battery Problem"
    )

    db.add(complaint)
    db.commit()

    assert complaint.complaint_id