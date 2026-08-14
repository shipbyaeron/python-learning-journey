import streamlit as st
import requests
import pandas as pd

st.title("Crypto P&L Tracker")

# Add description
st.write("Track your portfolio and P&L in real time.")

# Add text input
coin = st.text_input("Enter a coin ID:", "bitcoin")

# Show output
st.write("You entered:", coin)

# Button
if st.button("Get Price"):
    url = f"https://crypto-pnl-api.onrender.com/price/{coin}"
    response = requests.get(url)
    data = response.json()
    st.metric(label=f"{coin} price", value=data["price"])

# Show transactions
if st.button("Show All Transactions"):
    url = "https://crypto-pnl-api.onrender.com/transactions"
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)
    st.dataframe(df)

# POST new transaction
st.subheader("Log your new transaction here ⬇")

tx_coin = st.text_input("Coin name")
tx_action = st.selectbox("Action", ["buy", "sell"])
tx_amount = st.number_input("Amount")
tx_price = st.number_input("Price")

infor = {
    "coin": tx_coin,
    "action": tx_action,
    "amount": tx_amount,
    "price": tx_price
}

if st.button("Add Transaction"):
    url = "https://crypto-pnl-api.onrender.com/transaction"
    response = requests.post(url, json=infor)
    if response.status_code == 200:
        st.success("New transaction is saved successfully!")
    else:
        error_detail = response.json().get("detail", "Unknown error")
        st.error(f"Error: {error_detail}")
