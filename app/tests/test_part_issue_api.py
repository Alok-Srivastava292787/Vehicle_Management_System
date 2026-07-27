from fastapi.testclient import (    TestClient,)    #type: ignore

from app.main import app
client = TestClient(app)

def test_create_part_issue():

    response = client.post(
        "/api/v1/part-issues",
        json={
            "requisition_id": 1,
            "issued_by_employee_id": 1,
            "received_by_employee_id": 1,
            "status": "OPEN",
            "remarks": "Initial Issue",
        },
    )

    assert (
        response.status_code
        == 200
    )

    result = (
        response.json()
    )

    assert (
        result[
            "issue_number"
        ].startswith(
            "PI-"
        )
    )


def test_get_all_part_issues():

    response = client.get(
        "/api/v1/part-issues"
    )

    assert (
        response.status_code
        == 200
    )


def test_get_part_issue_not_found():

    response = client.get(
        "/api/v1/part-issues/999999"
    )

    assert (
        response.status_code
        == 404
    )


def test_get_part_issue():

    create_response = (
        client.post(
            "/api/v1/part-issues",
            json={
                "requisition_id": 1,
                "status": "OPEN",
            },
        )
    )

    issue = (
        create_response.json()
    )

    response = client.get(
        f"/api/v1/part-issues/"
        f"{issue['issue_id']}"
    )

    assert (
        response.status_code
        == 200
    )


def test_update_part_issue():

    create_response = (
        client.post(
            "/api/v1/part-issues",
            json={
                "requisition_id": 1,
                "status": "OPEN",
            },
        )
    )

    issue = (
        create_response.json()
    )

    response = client.put(
        f"/api/v1/part-issues/"
        f"{issue['issue_id']}",
        json={
            "status":
            "ISSUED",
        },
    )

    assert (
        response.status_code
        == 200
    )

    result = (
        response.json()
    )

    assert (
        result["status"]
        == "ISSUED"
    )


def test_delete_part_issue():

    create_response = (
        client.post(
            "/api/v1/part-issues",
            json={
                "requisition_id": 1,
                "status": "OPEN",
            },
        )
    )

    issue = (
        create_response.json()
    )

    response = client.delete(
        f"/api/v1/part-issues/"
        f"{issue['issue_id']}"
    )

    assert (
        response.status_code
        == 200
    )

    result = (
        response.json()
    )

    assert (
        result[
            "active_flag"
        ]
        is False
    )


def test_update_part_issue_not_found():

    response = client.put(
        "/api/v1/part-issues/999999",
        json={
            "status":
            "ISSUED",
        },
    )

    assert (
        response.status_code
        == 404
    )


def test_delete_part_issue_not_found():

    response = client.delete(
        "/api/v1/part-issues/999999"
    )

    assert (
        response.status_code
        == 404
    )