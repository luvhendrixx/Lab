import yfinance as yf 
import pandas as pd

nvda = yf.Ticker("NVDA")

data = nvda.history(period="1mo")

first_close = data["Close"].iloc[0]
last_close = data["Close"].iloc[-1] # give me the..last value (bc we start counting from 0, -1 means the last thing, you could use the index postition itself but..your keystrokes bruh)

daily_returns = data["Close"].pct_change() * 100

price_change = last_close - first_close

percent_change = (price_change / first_close) * 100

print(f"First close: {first_close}")
print(f"Last close: {last_close}")
print(f"Price change: {price_change}")
print(f"Percent change: {percent_change:.2f}%")
print(f"Daily returns: {daily_returns}")