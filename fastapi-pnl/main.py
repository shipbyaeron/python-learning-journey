from fastapi import FastAPI

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