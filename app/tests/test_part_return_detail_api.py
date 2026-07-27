from fastapi.testclient import (    TestClient,)    #type: ignore
from app.main import app
client = TestClient(app)
import random
def rand_n_digits(n: int) -> int:
    return random.randint(
        10 ** (n - 1),
        (10 ** n) - 1
    )
def test_create_part_return_detail():
    return_response = client.post(
        "/api/v1/part-returns",
        json={
            "issue_id": 1,
            "status": "OPEN",
        },
    )

    assert return_response.status_code == 200

    return_id = (
        return_response.json()["return_id"]
    )    
    payload={
            "return_id": return_id,
            "part_id": 1,
            "quantity_returned": 1,
            "serial_number": f"RET-SN-{rand_n_digits(3)}",
            "remarks": "Return Test",
        }

    response = client.post(
        "/api/v1/part-return-details",json=payload,
    )
    assert response.status_code == 200


def test_get_all_part_return_details():

    response = client.get(
        "/api/v1/part-return-details"
    )

    assert response.status_code == 200


def test_get_part_return_detail_not_found():

    response = client.get(
        "/api/v1/part-return-details/999999"
    )

    assert response.status_code == 404


def test_get_part_return_detail():

    create_response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 1,
        },
    )

    item = create_response.json()

    response = client.get(
        f"/api/v1/part-return-details/{item['return_detail_id']}"
    )

    assert response.status_code == 200


def test_update_part_return_detail():

    create_response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 1,
        },
    )

    item = create_response.json()
#    print(f"item:{item}")

    response = client.put(
        f"/api/v1/part-return-details/{item['return_detail_id']}",
        json={
            "quantity_returned": 5,
        },
    )
#    print(create_response.json())
#    print(response.json())
#    print(payload)

    assert response.status_code == 200

    assert (
        response.json()["quantity_returned"]
        == 5
    )


def test_delete_part_return_detail():

    create_response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 1,
        },
    )
    item = create_response.json()
    response = client.delete(
        f"/api/v1/part-return-details/{item['return_detail_id']}"
    )
    assert response.status_code == 200
    assert (
        response.json()["active_flag"]
        is False
    )


def test_update_part_return_detail_not_found():
    response = client.put(
        "/api/v1/part-return-details/999999",
        json={
            "quantity_returned": 15,
        },
    )
    assert response.status_code == 404


def test_delete_part_return_detail_not_found():
    response = client.delete(
        "/api/v1/part-return-details/999999"
    )
    assert response.status_code == 404

def test_return_part_not_issued():
    response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 9999,
            "quantity_returned": 1,
        },
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Part was not issued under this Issue"
    )

def test_return_qty_exceeds_issued_qty():
    response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 999,
        },
    )
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == (
            "Quantity Returned cannot "
            "exceed Quantity Issued"
        )
    )
def test_valid_return_quantity():
    response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 1,
        },
    )
    assert response.status_code == 200
    result = response.json()
    assert (
        result["quantity_returned"]
        == 1
    )
def test_cumulative_return_exceeds_issue_quantity():
    first = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 4,
        },
    )
    assert first.status_code == 200
    second = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 999,
        },
    )
    assert second.status_code == 400
    assert (
        second.json()["detail"]
        == (
            "Quantity Returned cannot "
            "exceed Quantity Issued"
        )
    )
def test_update_return_quantity_exceeds_issue():
    create_response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 1,
        },
    )
    detail = create_response.json()
    response = client.put(
        f"/api/v1/part-return-details/"
        f"{detail['return_detail_id']}",
        json={
            "quantity_returned": 999,
        },
    )
    assert response.status_code == 400

def test_return_quantity_zero():
    response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": 0,
        },
    )
    assert response.status_code == 400
def test_return_quantity_negative():
    response = client.post(
        "/api/v1/part-return-details",
        json={
            "return_id": 1,
            "part_id": 1,
            "quantity_returned": -5,
        },
    )

    assert response.status_code == 400