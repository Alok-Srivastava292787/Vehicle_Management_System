from fastapi.testclient import (
    TestClient,
)

from app.main import app

client = TestClient(app)


def test_create_driver():

    response = client.post(
        "/api/v1/drivers",
        json={
            "driver_name":
            "Test Driver",

            "mobile_number":
            "9999999999",
        },
    )

    assert (
        response.status_code
        == 201
    )