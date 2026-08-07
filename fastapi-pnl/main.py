from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

class Transaction(BaseModel):
    coin: str
    action: str
    amount: float
    price: float

app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Hello, this is my Crypto P&L API"}

@app.get("/hello")
def hello():
    return {"message":"Hello, today is a beautiful day!"}

@app.get("/about")
def about():
    return {"name":"Crypto P&L Tracker", "version":"v1.0", "feature":"Tracking crypto position & Calculating ROI", "author":"Aeron"}

@app.get("/coin/{coin_id}")
def get_coin(coin_id):
    return {"coin": coin_id}

@app.get("/double/{number}")
def double(number:int):
    return number * 2

@app.get("/greet")
def greet(name = "stranger"):
    return f"Hello, {name}"

@app.get("/coin/{coin_id}/convert")
def infor(coin_id, currency = "usd"):
    return {"coin": coin_id, "currency": currency}

@app.post("/transaction")
def create_transaction(tx: Transaction):
    if tx.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount value")
    elif tx.price <= 0:
        raise HTTPException(status_code=400, detail="Invalid price")
    else:
        total = tx.amount * tx.price
        return {"coin": tx.coin, "action": tx.action, "amount": tx.amount, "price": tx.price, "total": total}