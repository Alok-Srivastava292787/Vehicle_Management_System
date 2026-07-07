from fastapi.testclient import (
    TestClient,
)

from app.main import app
client = TestClient(app)

def test_create_inspection():

    response = client.post(
        "/api/v1/inspections",
        json={
            "complaint_id": 1,
            "technician_id": 1
        }
    )

    assert response.status_code == 201