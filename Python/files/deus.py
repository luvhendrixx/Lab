import json
import os
import websocket
from dotenv import load_dotenv

load_dotenv()
FINHUB_API = os.getenv("FINNHUB_API")

# Dynamic Tracking State

# tracks the highest price seens since starting the script
# it starts at 0.0 so any valid incoming price will immediately replace it
high_price = 0.0
low_price = float("inf") # inf means infinity
total_volume = 0.0 # a cummulative ctr that adds up the fraction of BTC traded in @ incoming exe
# remebers the exact price lvl where the last price spike alert triggered.
# set to None init bc no trades have arrived yet
last_alert_price = None

# Alert threshold: Notify if price moves by more than $500 from last alert
ALERT_THRESHOLD = 500.0

# runs auto every time Finnhub pushed new net pkts to my comp
# ws = websock instance that received the payload
# message = a raw txt string sent over the net
def on_message(ws, message):
    # tells python that mods inside this func should update the vars declared outside the func
    # ..preserving running totals across multiple msgs
    global high_price, low_price, total_volume, last_alert_price

    data = json.loads(message) # converts raw txt string into a native python dict
    if data.get("type") == "trade":
        # look at the docs for the chars used here
        for trade in data["data"]:
            symbol = trade["s"]
            price = float(trade["p"])
            volume = float(trade["v"])  # Finnhub sends volume in 'v'

            # Update rolling stats
            # cmpares what's inside the () then whichever is..max or min etc gets appeneded to the var (box)
            high_price = max(high_price, price)
            low_price = min(low_price, price)
            # adds the trades BTC vol to the cummulative running total
            total_volume += volume

            # Check for significant price movements
            if last_alert_price is None: # runs on the very first trade to est a baseline level of tracking
                last_alert_price = price

            # calcs numeric diff btwn incoming trade price and baseline price
            price_change = price - last_alert_price

            # checks if absolute magnitude of price shitft (+ or - ve) meets or exceeds the $500 threshold we set
            if abs(price_change) >= ALERT_THRESHOLD:
                direction = "🚀 UP" if price_change > 0 else "🔻 DOWN"
                print(
                    f"\n[ALERT] {symbol} moved {direction} by ${abs(price_change):.2f}! Current: ${price:.2f}\n"
                )
                last_alert_price = price

            # Print a clean summary instead of raw ticks in one line
            print(
                f"[{symbol}] Price: ${price:,.2f} | High: ${high_price:,.2f} | Low: ${low_price:,.2f} | Vol: {total_volume:.4f} BTC",
                end="\r", # this end="/r" (carriage return) moves the terminal cursor back to the beggining instead of jumping to a new line..its what enables the trade to be in one line
            )


def on_error(ws, error): # triggered if network drops, API key auths or invalid frames arrive..basically handles errors
    print("\nError:", error)


def on_close(ws, close_status_code, close_msg): # fires when the socket closes.e.g when ctrl + c is hit
    print("\n--- Connection Closed ---")

# runs immediately after est a connection to Finnhub sending the JSON txt fram to req the live ticker feed for BTC
def on_open(ws):
    print("Connected! Monitoring live BTC trades...")
    # what do you want to subscribe to?...BTC
    ws.send('{"type":"subscribe","symbol":"BINANCE:BTCUSDT"}')

# this code starts EXE from here
if __name__ == "__main__": # only exe's when python deus.py is run not when imported into another script
    if not FINHUB_API:
        raise ValueError("FINHUB_API not found! Check your .env file")

    websocket.enableTrace(False) # silences verbose logging onto the terminal
    ws = websocket.WebSocketApp(
        f"wss://ws.finnhub.io?token={FINHUB_API}",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )
    ws.on_open = on_open
    ws.run_forever() # speaks for itself