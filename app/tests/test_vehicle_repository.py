import uuid

from app.models.master import VehicleMaster
from app.repositories.vehicle_repository import (
    VehicleRepository,
)


def test_get_by_rc_number(db):

    vehicle = VehicleMaster(
        rc_number=f"TS-{uuid.uuid4()}",
    )

    repo = VehicleRepository(db)

    repo.create(vehicle)

    result = repo.get_by_rc_number(
        vehicle.rc_number
    )

    assert result is not None

    assert (
        result.rc_number
        == vehicle.rc_number
    )