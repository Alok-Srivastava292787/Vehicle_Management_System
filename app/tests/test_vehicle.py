from app.models.master import VehicleMaster


def test_create_vehicle(db):

    vehicle = VehicleMaster(
        rc_number="KA01AA0001",
        engine_no="ENG001",
        chassis_no="CH001"
    )

    db.add(vehicle)
    db.commit()
    db.refresh(vehicle)

    assert vehicle.vehicle_id is not None