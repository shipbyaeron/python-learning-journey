# Crypto P&L Tracker API

![CI](https://github.com/shipbyaeron/python-learning-journey/actions/workflows/ci.yml/badge.svg)

An all-in-one tracker for your crypto positions.

**Live demo v1.0:** https://crypto-pnl-api.onrender.com/docs

## Overview

The Crypto P&L Tracker API is built to become an ultimate crypto portfolio tracker for daily use.

The end goal is not just to manage your positions, but also to calculate the overall ROI of your portfolio. All numbers will be updated in real time using live market prices.

## Features

The API is now at **v1.0**. In this version, you can:

* Get the real-time price of any coin
* Log all your transactions, including both buy and sell
* View your transaction history anytime
* Update or delete transactions when needed

## Tech Stack

* **Framework:** FastAPI
* **Database:** PostgreSQL
* **Deployment:** Render + Docker

## API Endpoints

### 1. `/`

**Method:** GET

**Description:**
The default welcome message of the API.

### 2. `/about`

**Method:** GET

**Description:**
Returns basic information about the API, including its name, version, features, and author.

### 3. `/transaction`

**Method:** POST

**Description:**
Log a new transaction in the database.

The transaction details include:

* Coin name
* Action (buy or sell)
* Amount (total coin amount of the transaction)
* Price (buy or sell price)

The API will then calculate the total weight of the transaction:

`amount × price`

and return the result.

### 4. `/price/{coin_id}`

**Method:** GET

**Description:**
Get the real-time price of any coin using its `coin_id`.

The `coin_id` follows the IDs defined by CoinGecko, such as:

* `bitcoin`
* `ethereum`
* `solana`

If the coin doesn't exist or there is a typo, the API will return:

> "This coin doesn't exist. Try another one."

### 5. `/transactions`

**Method:** GET

**Description:**
Get the details of all transaction history.

### 6. `/transactions/{id}`

**Method:** GET

**Description:**
Each transaction has its own ID. You can query any transaction by entering its ID.

The API will return the details of the corresponding transaction.

### 7. `/transactions/{id}`

**Method:** DELETE

**Description:**
Delete any transaction by entering its ID.

### 8. `/transactions/{id}`

**Method:** PUT

**Description:**
Update any transaction when you need to fix or change its details.

To do this, you need to provide the transaction ID and the new details you want to update.

The API will return a success message once the transaction has been successfully updated.

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/shipbyaeron/python-learning-journey.git
cd python-learning-journey/fastapi-pnl
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file with:

```env
DATABASE_URL=your_postgres_connection_string
COINGECKO_API_KEY=your_coingecko_api_key
```

### 5. Run the server

```bash
uvicorn main:app --reload
```

### 6. Open the API documentation

Go to:

`http://127.0.0.1:8000/docs`

From there, you can explore and test the API.

## Future Improvements

### 1. Entry Price & Position ROI

At the moment, all transactions are disconnected from each other.

For the next version, if multiple transactions have the same coin ID, the API will automatically calculate the average entry price based on the transaction details.

From there, combined with the real-time price from CoinGecko, users will be able to see the ROI of each position, including whether it is in the red or green and by how much.

### 2. Portfolio ROI

The transaction details will give a clear picture of the principal capital a user has put into their portfolio.

Combined with the position ROI, the API will calculate and return the overall ROI of the entire portfolio.

All of this will be updated in real time thanks to the CoinGecko API.

### 3. TP/SL

The vision goes beyond just managing a portfolio. I also want this API to help users rebalance their positions.

The end goal is to connect the API with a trading bot, where users can set TP (Take Profit) or SL (Stop Loss) for each position.

Once the price reaches the target, the API will execute the order through the trading bot and update the portfolio accordingly.

All information will be communicated to the users before and after the order goes through.

## Final Vision

The current version is just the beginning.

The goal is to gradually turn this from a simple transaction tracker into a complete crypto portfolio management system, where users can track their positions, understand their P&L, monitor their portfolio ROI, and eventually automate their trading strategy.