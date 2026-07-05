
from app.models.master import DriverMaster


def test_create_driver(db):

    driver = DriverMaster(
        driver_name="Test Driver",
        mobile_number="9999999999",
        dl_number="DL123456"
    )

    db.add(driver)
    db.commit()
    db.refresh(driver)

    assert driver.driver_id is not None
