from app.models.inventory import PartMaster, PartRequest
from app.models.master import VehicleMaster,EmployeeMaster
from app.db.session import SessionLocal
import uuid
from datetime import datetime

def inventory_workflow_test(db):
    #create
    part = PartMaster(
        part_code=f"BAT-{datetime.now().timestamp()}",
        part_name="Battery"
    )

    employee = EmployeeMaster(
            full_name="Johny",
            phone_number="9099999909"
        )

    vehicle = VehicleMaster(
        rc_number=f"KA01-{uuid.uuid4()}"
    )
    
    session=SessionLocal()
    session.add(part)
    session.commit()

    #then
    request = PartRequest(
        request_number="REQ001",
        vehicle_id=vehicle.vehicle_id,
        request_id=employee.employee_id
    )

    session.add(request)
    session.commit()
