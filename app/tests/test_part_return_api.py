from fastapi.testclient import (    TestClient,)    #type: ignore
from app.main import app
client = TestClient(app)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
    )

def test_create_part_return():

    response = client.post(
        "/api/v1/part-returns",
        json={
            "issue_id": 1,
            "returned_by_employee_id": 1,
            "received_by_employee_id": 1,
            "status": "OPEN",
            "remarks": "Initial Return",
#            "return_id": 1,
        },
    )
#    print(response.json())
    assert response.status_code == 200

    result = response.json()

    assert (
        result["return_number"]
        .startswith("PRT-")
    )


def test_get_all_part_returns():

    response = client.get(
        "/api/v1/part-returns"
    )

    assert response.status_code == 200


def test_get_part_return_not_found():

    response = client.get(
        "/api/v1/part-returns/999999"
    )

    assert response.status_code == 404


def test_get_part_return():

    create_response = client.post(
        "/api/v1/part-returns",
        json={
            "issue_id": 1,
            "status": "OPEN",
        },
    )

    item = create_response.json()

    response = client.get(
        f"/api/v1/part-returns/{item['return_id']}"
    )

    assert response.status_code == 200


def test_update_part_return():

    create_response = client.post(
        "/api/v1/part-returns",
        json={
            "issue_id": 1,
            "status": "OPEN",
        },
    )

    item = create_response.json()

    response = client.put(
        f"/api/v1/part-returns/{item['return_id']}",
        json={
            "status": "CLOSED",
        },
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "CLOSED"
    )


def test_delete_part_return():

    create_response = client.post(
        "/api/v1/part-returns",
        json={
            "issue_id": 1,
            "status": "OPEN",
        },
    )

    item = create_response.json()

    response = client.delete(
        f"/api/v1/part-returns/{item['return_id']}"
    )

    assert response.status_code == 200

    assert (
        response.json()["active_flag"]
        is False
    )


def test_update_part_return_not_found():

    response = client.put(
        "/api/v1/part-returns/999999",
        json={
            "status": "CLOSED"
        },
    )

    assert response.status_code == 404


def test_delete_part_return_not_found():

    response = client.delete(
        "/api/v1/part-returns/999999"
    )

    assert response.status_code == 404