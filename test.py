import yfinance as yf

stock = yf.Ticker("RELIANCE.NS")

price = stock.history(period="1d")["Close"].iloc[-1]

print("Current Price:", price)