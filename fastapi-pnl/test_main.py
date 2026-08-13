from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, this is my Crypto P&L API"}

def test_about():
    response = client.get("/about")
    assert response.status_code == 200
    assert response.json() == {"name":"Crypto P&L Tracker", "version":"v1.0", "feature":"Tracking crypto position & Calculating ROI", "author":"Aeron"}

def test_get_price_success():
    response = client.get("/price/bitcoin")
    assert response.status_code == 200
    assert type(response.json()["coin"]) == str
    assert type(response.json()["price"]) in (int, float)

def test_get_price_fail():
    response = client.get("/price/notacoin")
    assert response.status_code == 404
    assert response.json() == {"detail": "This coin doesn't exist. Try another one."}

def test_post_transactions_invalid_amount():
    response = client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": -5, "price": 64000})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid amount value"}

def test_post_transactions_invalid_price():
    response = client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": 0.5, "price": -64000})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid price"}