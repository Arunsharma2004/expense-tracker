from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_server_is_running():
    response = client.get("/expenses")
    assert response.status_code == 200

def test_create_expense():
    response = client.post("/expenses", json={
        "amount": 25.50,
        "category": "groceries",
        "date": "2026-08-12"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["amount"] == 25.50
    assert data["category"] == "groceries"
    assert "id" in data

def test_create_expense_invalid_category():
    response = client.post("/expenses", json={
        "amount": 25.50,
        "category": "Supliments",
        "date": "2026-08-12"
    })
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_create_expense_negative_amount():
    response = client.post("/expenses", json={
        "amount": -50,
        "category": "groceries",
        "date": "2026-08-12"
    })
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_delete_nonexistent_expense():
    response = client.delete("/expenses/999")
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_get_summary():
    response = client.get("/summary?month=8&year=2026")
    assert response.status_code == 200