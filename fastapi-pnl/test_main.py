import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
import pytest
from fastapi.testclient import TestClient
from main import app, get_db

load_dotenv()
dataTestURL = os.getenv("TEST_DATABASE_URL")

def get_test_db():
    conn = psycopg2.connect(dataTestURL, cursor_factory=RealDictCursor)
    try: 
        yield conn
    finally:
        conn.close()

app.dependency_overrides[get_db] = get_test_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clean_db():
    conn = psycopg2.connect(dataTestURL)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id SERIAL PRIMARY KEY, coin TEXT, action TEXT, amount NUMERIC, price NUMERIC, total NUMERIC)")
    cursor.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
    yield

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

def test_post_transaction_invalid_amount():
    response = client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": -5, "price": 64000})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid amount value"}

def test_post_transaction_invalid_price():
    response = client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": 0.5, "price": -64000})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid price"}

def test_post_transaction():
    response = client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": 0.5, "price": 64000})
    assert response.status_code == 200
    assert response.json()["total"] == 32000

def test_get_transactions():
    client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": 0.5, "price": 64000})
    response = client.get("/transactions")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["coin"] == "bitcoin"

def test_get_tx_by_id():
    client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": 0.5, "price": 64000})
    rows = client.get("/transactions")
    id = rows.json()[0]["id"]
    response = client.get(f"/transactions/{id}")
    assert response.status_code == 200
    assert response.json() == {"id": id, "coin": "bitcoin", "action": "buy", "amount": 0.5, "price": 64000, "total": 32000}

def test_delete_tx_by_id():
    client.post("/transaction", json={"coin": "bitcoin", "action": "buy", "amount": 0.5, "price": 64000})
    rows_before = client.get("/transactions")
    id = rows_before.json()[0]["id"]
    response = client.delete(f"/transactions/{id}")
    assert response.status_code == 200
    rows_after = client.get("/transactions")
    assert len(rows_after.json()) == 0