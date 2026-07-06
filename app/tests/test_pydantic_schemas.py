from app.schemas.vehicle import VehicleCreate


def test_vehicle_schema():

    payload = VehicleCreate(
        rc_number="KA01AB1234"
    )

    assert payload.rc_number == "KA01AB1234"