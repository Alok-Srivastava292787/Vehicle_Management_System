from fastapi.testclient import (    TestClient,)    #type: ignore

from app.main import app
client = TestClient(app)

def test_create_opening_stock():

    response = client.post(
        "/api/v1/opening-stock",
        json={
            "part_id": 26,
            "opening_quantity": 500,
            "remarks": "Initial Stock",
        },
    )
#    print(response.json())
    assert response.status_code == 200


def test_get_all_opening_stock():

    response = client.get(
        "/api/v1/opening-stock"
    )

    assert response.status_code == 200


def test_get_opening_stock_not_found():

    response = client.get(
        "/api/v1/opening-stock/999999"
    )

    assert response.status_code == 404


def test_get_opening_stock():

    create_response = client.post(
        "/api/v1/opening-stock",
        json={
            "part_id": 27,
            "opening_quantity": 100,
        },
    )

    item = create_response.json()

    response = client.get(
        f"/api/v1/opening-stock/{item['opening_stock_id']}"
    )

    assert response.status_code == 200


def test_update_opening_stock():

    create_response = client.post(
        "/api/v1/opening-stock",
        json={
            "part_id": 28,
            "opening_quantity": 50,
        },
    )

    item = create_response.json()

    response = client.put(
        f"/api/v1/opening-stock/{item['opening_stock_id']}",
        json={
            "remarks":
            "Updated",
        },
    )

    assert response.status_code == 200


def test_delete_opening_stock():

    create_response = client.post(
        "/api/v1/opening-stock",
        json={
            "part_id": 29,
            "opening_quantity": 500,
            "remarks": "Initial Stock",
        },
    )

#    print(create_response.status_code)
#    print(create_response.text)
#    print(create_response.json())
    item = create_response.json()
#    print(item)
    response = client.delete(
        f"/api/v1/opening-stock/{item['opening_stock_id']}"
    )
#    print(response.json())
    assert response.status_code == 200


def test_opening_stock_duplicate_part():

    client.post(
        "/api/v1/opening-stock",
        json={
            "part_id": 30,
            "opening_quantity": 500,
            "remarks": "Initial Stock",
        },
    )

    response = client.post(
        "/api/v1/opening-stock",
        json={
            "part_id": 30,
            "opening_quantity": 200,
        },
    )

    assert response.status_code == 400