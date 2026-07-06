import uuid

from app.models.master import DriverMaster
from app.repositories.driver_repository import (
    DriverRepository,
)


def test_driver_by_dl(db):

    driver = DriverMaster(
        driver_name="Test Driver",
        mobile_number="9999999999",
        dl_number=f"DL-{uuid.uuid4()}",
    )

    repo = DriverRepository(db)

    repo.create(driver)

    assert driver.dl_number is not None
    
    result = repo.get_by_dl_number(
        driver.dl_number
    )
    assert result is not None
