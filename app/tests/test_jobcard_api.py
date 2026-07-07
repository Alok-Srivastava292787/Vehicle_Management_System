from fastapi.testclient import (
    TestClient,
)

from app.main import app
client = TestClient(app)

def test_create_jobcard():

    response = client.post(
        "/api/v1/jobcards",
        json={
            "complaint_id": 1,
            "inspection_id": 1,
            "vehicle_id": 1
        }
    )

    assert response.status_code == 201