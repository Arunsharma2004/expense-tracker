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

def test_update_expense():
    create_response = client.post("/expenses", json={
        "amount": 25.50,
        "category": "groceries",
        "date": "2026-08-12"
    })
    expense_id = create_response.json()["id"]

    response = client.put(f"/expenses/{expense_id}", json={
        "amount": 40.00,
        "category": "transport",
        "date": "2026-08-13"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 40.00
    assert data["category"] == "transport"
    assert data["date"] == "2026-08-13"
    assert data["id"] == expense_id

def test_update_nonexistent_expense():
    response = client.put("/expenses/999", json={
        "amount": 40.00,
        "category": "transport",
        "date": "2026-08-13"
    })
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data

def test_update_expense_invalid_category():
    create_response = client.post("/expenses", json={
        "amount": 25.50,
        "category": "groceries",
        "date": "2026-08-12"
    })
    expense_id = create_response.json()["id"]

    response = client.put(f"/expenses/{expense_id}", json={
        "amount": 40.00,
        "category": "Supliments",
        "date": "2026-08-13"
    })
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_create_budget():
    response = client.post("/budgets", json={
        "category": "groceries",
        "amount": 500,
        "month": 8,
        "year": 2026
    })
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "groceries"
    assert data["amount"] == 500
    assert "id" in data

def test_check_budget():
    client.post("/budgets", json={
    "category": "groceries",
    "amount": 300,
    "month": 8,
    "year": 2026
    })
    client.post("/expenses", json={
    "amount": 250,
    "category": "groceries",
    "date": "2026-08-15"
    })
    response = client.get("/budgets?category=groceries&month=8&year=2026")
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "groceries"
    assert data["month"] == 8
    assert data["year"] == 2026
    assert data["spent"] >= 250