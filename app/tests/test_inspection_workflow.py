from app.models.maintenance import TechnicianInspection, VehicleComplaint
from app.models.master import VehicleMaster,DriverMaster, EmployeeMaster

from app.db.session import SessionLocal 

def test_create_complaint(db):
    vehicle = VehicleMaster(
        rc_number="KA01AA1002"
    )

    driver = DriverMaster(
        driver_name="John",
        mobile_number="8888888888"
    )

    employee = EmployeeMaster(
        full_name="Johny",
        phone_number="9099999999"
    )

    db.add_all([vehicle, driver, employee])
    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery issue"
    )

    db.add(complaint)
    db.commit()


    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=employee.employee_id,
        observed_issue="Dead Battery"
    )

    session=SessionLocal()
    session.add(inspection)
    session.commit()