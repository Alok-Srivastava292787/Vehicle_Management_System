from fastapi.testclient import (
    TestClient,
)

from app.main import app
import uuid
client = TestClient(app)


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