from fastapi.testclient import (
    TestClient,
)

from app.main import app
client = TestClient(app)

import uuid

def test_create_vehicle():

    response = client.post(
        "/api/v1/vehicles",
        json={
            "rc_number":
            f"TEST-{uuid.uuid4()}",
            
            "engine_no":
            f"ENG-{uuid.uuid4()}",

            "chassis_no":
            f"CH-{uuid.uuid4()}"
        },
    )

    assert (
        response.status_code
        == 201
    )

def test_create_driver():

    response = client.post(
        "/api/v1/drivers",
        json={
            "driver_name":
            "Test Driver",

            "mobile_number":
            "9999999999",
            
            "dl_number":
            f"DL-{uuid.uuid4()}",
        },
    )

    assert (
        response.status_code
        == 201
    )

response = client.post(
    "/api/v1/complaints",
    json={
        "vehicle_id": 1,
        "driver_id": 1,
        "issue_description":
        "Battery issue",
    },
)