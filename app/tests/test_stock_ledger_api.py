from fastapi.testclient import (    TestClient,)    #type: ignore

from app.main import app
client = TestClient(app)

def test_create_stock_ledger():

    response = client.post(
        "/api/v1/stock-ledger",
        json={
            "part_id": 2,
            "transaction_type": "OPENING",
            "reference_id": 2,
            "quantity_in": 100,
            "quantity_out": 0,
            "balance_quantity": 100,
            "remarks": "Opening Stock",
        },
    )
    print(response.json())
    assert response.status_code == 200


def test_get_stock_ledger():

    response = client.get(
        "/api/v1/stock-ledger"
    )

    assert response.status_code == 200


def test_get_stock_ledger_not_found():

    response = client.get(
        "/api/v1/stock-ledger/999999"
    )

    assert response.status_code == 404


def test_update_stock_ledger():

    create_response = client.post(
        "/api/v1/stock-ledger",
        json={
            "part_id": 1,
            "transaction_type": "OPENING",
            "quantity_in": 100,
            "balance_quantity": 100,
        },
    )

    item = create_response.json()

    response = client.put(
        f"/api/v1/stock-ledger/{item['ledger_id']}",
        json={
            "remarks":
            "Updated",
        },
    )

    assert response.status_code == 200


def test_delete_stock_ledger():

    create_response = client.post(
        "/api/v1/stock-ledger",
        json={
            "part_id": 1,
            "transaction_type": "OPENING",
            "quantity_in": 100,
            "balance_quantity": 100,
        },
    )

    item = create_response.json()

    response = client.delete(
        f"/api/v1/stock-ledger/{item['ledger_id']}"
    )

    assert response.status_code == 200


def test_get_balance():

    response = client.get(
        "/api/v1/stock-ledger/balance/1"
    )

    assert response.status_code == 200