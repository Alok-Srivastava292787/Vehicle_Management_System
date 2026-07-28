from fastapi.testclient import (    TestClient,)    #type: ignore

from app.main import app
client = TestClient(app)


def test_create_part_issue_detail():

    response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 1,
            "quantity_issued": 5,
            "serial_number": "ISS-SN-001",
            "remarks": "Issue Test",
        },
    )

    assert response.status_code == 200


def test_get_all_part_issue_details():

    response = client.get(
        "/api/v1/part-issue-details"
    )

    assert response.status_code == 200


def test_get_part_issue_detail_not_found():

    response = client.get(
        "/api/v1/part-issue-details/999999"
    )

    assert response.status_code == 404


def test_get_part_issue_detail():

    create_response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 1,
            "quantity_issued": 2,
        },
    )

    detail = create_response.json()

    response = client.get(
        f"/api/v1/part-issue-details/{detail['issue_detail_id']}"
    )

    assert response.status_code == 200


def test_update_part_issue_detail():

    create_response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 1,
            "quantity_issued": 2,
        },
    )

    detail = create_response.json()

    response = client.put(
        f"/api/v1/part-issue-details/{detail['issue_detail_id']}",
        json={
            "quantity_issued": 10,
        },
    )

    assert response.status_code == 200

    assert (
        response.json()[
            "quantity_issued"
        ]
        == 10
    )


def test_delete_part_issue_detail():

    create_response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 1,
        },
    )

    detail = create_response.json()

    response = client.delete(
        f"/api/v1/part-issue-details/{detail['issue_detail_id']}"
    )

    assert response.status_code == 200

    assert (
        response.json()[
            "active_flag"
        ]
        is False
    )


def test_update_part_issue_detail_not_found():

    response = client.put(
        "/api/v1/part-issue-details/999999",
        json={
            "quantity_issued": 99,
        },
    )

    assert response.status_code == 404


def test_delete_part_issue_detail_not_found():

    response = client.delete(
        "/api/v1/part-issue-details/999999"
    )

    assert response.status_code == 404
def test_issue_part_not_in_requisition():

    response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 999999,
            "quantity_issued": 1,
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Part not found in Requisition"
    )
def test_issue_qty_exceeds_request():

    response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 1,
            "quantity_issued": 999,
        },
    )

    assert response.status_code == 400

    assert (
        response.json()["detail"]
        ==
        "Issued Quantity cannot exceed Requested Quantity"
    )
def test_issue_quantity_zero():

    response = client.post(
        "/api/v1/part-issue-details",
        json={
            "issue_id": 1,
            "part_id": 1,
            "quantity_issued": 0,
        },
    )

    assert response.status_code == 400
