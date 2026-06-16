import os
import matplotlib.pyplot as plt
import yfinance as yf
import streamlit as st
import pandas as pd

if "portfolio" not in st.session_state:

    if os.path.exists("portfolio.csv"):

        st.session_state.portfolio = pd.read_csv(
            "portfolio.csv"
        ).to_dict("records")

    else:

        st.session_state.portfolio = []

 #for stock in portfolio:
 #   stock["Profit"] = (
  #      stock["Qty"] * stock["Current"]
   #     - stock["Qty"] * stock["Buy"]
    #)

total_invested = 0
total_value = 0
total_profit = 0

for stock in st.session_state.portfolio:

    invested = stock["Qty"] * stock["Buy"]

    total_invested += invested

    total_value += stock["Qty"] * stock["Current"]

    total_profit += stock.get("Profit", 0) 

if total_invested > 0:
    return_percent = (
        total_profit / total_invested
    ) * 100
else:
    return_percent = 0    

st.title("📈 Stock Portfolio Dashboard")

stock_name = st.text_input("Stock Name")

qty = st.number_input("Quantity", min_value=1)

buy_price = st.number_input("Buy Price", min_value=0.0)

if st.button("Add Stock"):

    ticker = yf.Ticker(stock_name.upper() + ".NS")

    current_price = ticker.history(period="1d")["Close"].iloc[-1]

    profit = (qty * current_price) - (qty * buy_price)

    stock = {
        "Stock": stock_name.upper(),
        "Qty": qty,
        "Buy": buy_price,
        "Current": round(current_price, 2),
        "Profit": round(profit, 2)
    }

    st.session_state.portfolio.append(stock)

    df_save = pd.DataFrame(st.session_state.portfolio)

    df_save.to_csv("portfolio.csv", index=False)

    st.write("Portfolio Length:", len(st.session_state.portfolio))

if st.button("🔄 Refresh Prices"):

    for stock in st.session_state.portfolio:

        ticker = yf.Ticker(stock["Stock"] + ".NS")

        current_price = ticker.history(period="1d")["Close"].iloc[-1]

        stock["Current"] = round(current_price, 2)

        stock["Profit"] = round(
            (stock["Qty"] * current_price)
            - (stock["Qty"] * stock["Buy"]),
            2
        )

    pd.DataFrame(
        st.session_state.portfolio
    ).to_csv(
        "portfolio.csv",
        index=False
    )

    st.success("Prices Updated!")

    st.rerun()    

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Invested",
        f"₹{total_invested:,.2f}"
    )

with col2:
    st.metric(
        "Portfolio Value",
        f"₹{total_value:,.2f}"
    )

with col3:
    st.metric(
        "Total Profit",
        f"₹{total_profit:,.2f}"
    )

with col4:
    st.metric(
        "Return %",
        f"{return_percent:.2f}%"
    )    

st.write("Welcome to my first fintech project 🚀")

df = pd.DataFrame(st.session_state.portfolio)


if not df.empty:

   chart_data = df.set_index("Stock")["Profit"]

   st.subheader("Profit by Stock")

   st.bar_chart(chart_data)

   if not df.empty:

    allocation = df["Qty"] * df["Current"]

    fig, ax = plt.subplots()

    ax.pie(
        allocation,
        labels=df["Stock"],
        autopct="%1.1f%%"
    )

    ax.set_title("Portfolio Allocation")

    st.pyplot(fig)

    st.dataframe(df)

    if not df.empty:

        stock_to_delete = st.selectbox(
        "Select stock to delete",
        df["Stock"]
    )

    if st.button("Delete Stock"):

        st.session_state.portfolio = [
            stock
            for stock in st.session_state.portfolio
            if stock["Stock"] != stock_to_delete
        ]

        pd.DataFrame(
            st.session_state.portfolio
        ).to_csv(
            "portfolio.csv",
            index=False
        )

        st.rerun()

csv = df.to_csv(index=False)

st.download_button(
    label="📥 Download Portfolio CSV",
    data=csv,
    file_name="portfolio.csv",
    mime="text/csv"
)

  

