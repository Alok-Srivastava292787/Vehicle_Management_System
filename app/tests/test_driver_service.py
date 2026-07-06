import uuid

from app.schemas.driver import (
    DriverCreate,
)

from app.repositories.driver_repository import (
    DriverRepository,
)

from app.services.driver_service import (
    DriverService,
)


def test_create_driver_service(
    db
):

    repo = DriverRepository(db)

    service = DriverService(
        repo
    )

    payload = DriverCreate(
        driver_name="Driver",
        mobile_number="9999999999",
        dl_number=f"DL-{uuid.uuid4()}",
    )

    driver = (
        service.create_driver(
            payload
        )
    )

    assert driver.driver_id