from fastapi.testclient import (
    TestClient,
)

from app.main import app
client = TestClient(app)

def test_create_checklist():

    response = client.post(
        "/api/v1/checklists",
        json={
            "vehicle_id": 1,
            "technician_id": 1
        }
    )

    assert response.status_code == 201