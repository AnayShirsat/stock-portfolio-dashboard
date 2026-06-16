import yfinance as yf
portfolio = []

while True:

    stock_name = input("Enter stock name : ")
    qty = int(input("Enter quantity : "))
    buy_price = float(input("Enter buy price : "))
  
    ticker = yf.Ticker(stock_name + ".NS")
    current_price = ticker.history(period="1d")["Close"].iloc[-1]

    print("Live Price:", current_price)

    stock = {
        "stock": stock_name,
        "qty": qty,
        "buy": buy_price,
        "current": current_price
    }

    portfolio.append(stock)

    choice = input("Add another stock? (y/n): ")

    if choice.lower() == "n":
        break

print(portfolio)
total_invested = 0
total_current = 0

for stock in portfolio:

    invested = stock["qty"] * stock["buy"]
    current_value = stock["qty"] * stock["current"]
    profit = current_value - invested

    total_invested += invested
    total_current += current_value

    print("\nStock:", stock["stock"])
    print("Invested: ₹", round(invested, 2))
    print("Current Value: ₹", round(current_value, 2))
    print("Profit: ₹", round(profit, 2))
    total_profit = total_current - total_invested

print("\nPortfolio Summary")
print("Total Invested: ₹", round(total_invested, 2))
print("Total Current Value: ₹", round(total_current, 2))
print("Total Profit: ₹", round(total_profit, 2))