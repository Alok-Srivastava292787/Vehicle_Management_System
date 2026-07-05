from app.models.operations import DriverVehicleAssignment
from app.models.master import DriverMaster, VehicleMaster

def test_driver_assignment_fk(db):

    driver = DriverMaster(
        driver_name="Test Driver",
        mobile_number="9999999999"
    )

    vehicle = VehicleMaster(
        rc_number="KA01AA1001"
    )

    db.add(driver)
    db.add(vehicle)
    db.commit()

    assignment = DriverVehicleAssignment(
        driver_id=driver.driver_id,
        vehicle_id=vehicle.vehicle_id
    )

    db.add(assignment)
    db.commit()

    assert assignment.assignment_id is not None

