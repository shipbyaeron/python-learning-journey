from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()
dataURL = os.getenv("DATABASE_URL")

API_KEY = os.getenv("APP_API_KEY")
if not API_KEY:
    raise ValueError("Security error! Pls add the APP_API_KEY to .env to run this")

class Transaction(BaseModel):
    coin: str
    action: str
    amount: float
    price: float

app = FastAPI()

def get_db():
    conn = psycopg2.connect(dataURL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    conn = psycopg2.connect(dataURL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id SERIAL PRIMARY KEY, coin TEXT, action TEXT, amount NUMERIC, price NUMERIC, total NUMERIC)")
    conn.commit()
    conn.close()

init_db()

def check_auth(x_api_key: str | None = Header(None)):
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key!")

@app.get("/")
def read_root():
    return {"message":"Hello, this is my Crypto P&L API"}

@app.get("/about")
def about():
    return {"name":"Crypto P&L Tracker", "version":"v1.0", "feature":"Tracking crypto position & Calculating ROI", "author":"Aeron"}

@app.post("/transaction", dependencies=[Depends(check_auth)])
def create_transaction(tx: Transaction, conn = Depends(get_db)):
    if tx.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount value")
    elif tx.price <= 0:
        raise HTTPException(status_code=400, detail="Invalid price")
    else:
        total = tx.amount * tx.price
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (coin, action, amount, price, total) VALUES (%s, %s, %s, %s, %s)", 
            (tx.coin, tx.action, tx.amount, tx.price, total)
        )
        conn.commit()
        return {"message": "Transactions are saved", "coin": tx.coin, "action": tx.action, "amount": tx.amount, "price": tx.price, "total": total}
    
@app.get("/price/{coin_id}")
def get_price(coin_id):
    priceUrl = "https://api.coingecko.com/api/v3/simple/price"
    headers = {"x-cg-demo-api-key": os.getenv("COINGECKO_API_KEY")}
    params = {
        "ids": coin_id,
        "vs_currencies": "usd"
    }
    response = requests.get(priceUrl, headers=headers, params=params)
    priceData = response.json()

    if coin_id not in priceData:
        raise HTTPException(status_code=404, detail="This coin doesn't exist. Try another one.")
    else:
        return {"coin": coin_id, "price": priceData[coin_id]["usd"]}

@app.get("/transactions", dependencies=[Depends(check_auth)])
def get_transaction(conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions")
    rows = cursor.fetchall()
    return rows

@app.get("/transactions/{id}", dependencies=[Depends(check_auth)])
def get_tx_by_id(id:int, conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        return row
    else:
        raise HTTPException(status_code=404, detail="Invalid id number")

@app.delete("/transactions/{id}", dependencies=[Depends(check_auth)])
def del_tx(id:int, conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        cursor.execute("DELETE FROM transactions WHERE id = %s", (id,))
        conn.commit()
        return {"message": f"Delete transaction {id} successfully"}
    else:
        raise HTTPException(status_code=404, detail="Invalid id number")

@app.put("/transactions/{id}", dependencies=[Depends(check_auth)])
def alter_tx(id:int, tx: Transaction, conn = Depends(get_db)):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transactions WHERE id = %s", (id,))
    row = cursor.fetchone()
    if row:
        new_total = tx.amount * tx.price
        cursor.execute("UPDATE transactions SET coin = %s, action = %s, amount = %s, price = %s, total = %s WHERE id = %s", (tx.coin, tx.action, tx.amount, tx.price, new_total, id,))
        conn.commit()
        return {"message": f"Transaction {id} is updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Invalid id number")