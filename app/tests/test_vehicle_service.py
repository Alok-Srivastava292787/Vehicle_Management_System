import uuid

from app.schemas.vehicle import (
    VehicleCreate,
)

from app.repositories.vehicle_repository import (
    VehicleRepository,
)

from app.services.vehicle_service import (
    VehicleService,
)


def test_create_vehicle_service(
    db
):

    repo = VehicleRepository(db)

    service = VehicleService(
        repo
    )

    payload = VehicleCreate(
        rc_number=f"TS-{uuid.uuid4()}"
    )

    vehicle = (
        service.create_vehicle(
            payload
        )
    )

    assert vehicle.vehicle_id