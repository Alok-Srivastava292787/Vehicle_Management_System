from app.models.maintenance import MaintenanceJobCard,VehicleComplaint, TechnicianInspection
from app.models.master import VehicleMaster,DriverMaster,EmployeeMaster
from app.db.session import SessionLocal
import uuid
def test_create_job_card(db):
    vehicle = VehicleMaster(
        rc_number=f"TEST-{uuid.uuid4()}",
        engine_no=f"ENG-{uuid.uuid4()}",
        chassis_no=f"CH-{uuid.uuid4()}"
    )

    driver = DriverMaster(
        driver_name="John",
        mobile_number="8888888888"
    )
    
    employee = EmployeeMaster(
        employee_type="TECHNICIAN",
        full_name="John Doe",
        phone_number="9999999999"
    )


    db.add_all([vehicle, driver, employee])
    db.commit()

    complaint = VehicleComplaint(
        vehicle_id=vehicle.vehicle_id,
        driver_id=driver.driver_id,
        issue_description="Battery issue"
    )

    inspection = TechnicianInspection(
        complaint_id=complaint.complaint_id,
        technician_id=employee.employee_id,
        observed_issue="Battery dead",
        operator_notes="Needs replacement",
        status="OPEN"
    )

    db.add_all([complaint, inspection])
    db.commit()


    job_card = MaintenanceJobCard(
    complaint_id=complaint.complaint_id,
    inspection_id=inspection.inspection_id,
    job_card_id=98
    )

    session=SessionLocal()
    session.add(job_card)
    session.commit()

