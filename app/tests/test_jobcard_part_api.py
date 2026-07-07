from fastapi.testclient import (
    TestClient,
)

from app.main import app
client = TestClient(app)

def test_create_jobcard_part():

    response = client.post(
        "/api/v1/jobcard-parts",
        json={
            "job_card_id": 1,
            "part_id": 1,
            "quantity": 2,
            "unit_price": 100,
        }
    )

    assert response.status_code == 201