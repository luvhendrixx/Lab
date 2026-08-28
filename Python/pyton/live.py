import asyncio
import json
import websockets # type: ignore

'''
set keeps track of active connections

we use a set over list bc sets enforce unique values
(prevening duplicate connections) and follow instantaneous + or removal of connections
'''
CONNECTED_BROWSERS = set() # prevents duplicates and is blazing fast since theres no index but stores them randomly using a background proc called hashing making lookups really fast


'''
async def declares as async func (co-routine). You can't use await INSIDE standard def functions
'''
async def binance_listener():
    # listens to binance and broadcasts every trade to the connected browsers
    url = "wss://stream.binance.com:9443/ws/btcusdt@trade"


    '''
    async context manager. It opens the Websock client connection to Binance
    and ensures that if the loop breaks or crashes, the socket connection closes cleanly
    '''
    async with websockets.connect(url) as binance_ws:
        print("Connected to Binance! Waiting for browsers.....")


        while True: # creates the inifinite loop to contstantly listen for new trades
            '''
            await binance_ws.recv() pauses exe at this exact line until Binance pushes
            a new msg down the wire. While waiting, python's CPU context switches to other tasks...co-currency
            '''
            message = await binance_ws.recv() # wait for whatver binance_ws receives
            data = json.loads(message) # parsing of the data we receive

            price = float(data['p']) # extracts string price from binance trade payload & casts it to a float
            print(f"[PYTHON BACKEND] Received BTC Price: ${price:,.2f}")

            # send the price data to every connected browser
            if CONNECTED_BROWSERS: # skips broadcasting if no browsers are connected to save CPU cycles
                payload = json.dumps({"price": price}) # formating happens here

                # broadcast concurrently to all browser connections
                await asyncio.gather(
                    # sends the payload to every browser in CONNECTED_BROWSERS simultaneuosly in parrarel
                    # rather than waiting for browser #1 to reply before sending to browser #2
                    *[browser.send(payload) for browser in CONNECTED_BROWSERS]
                )

'''
Everytime a browser connects to the computer, the websock server runs this func,
passing that specific browsers connection object as websocket
'''
async def handle_browser(websocket):
    # handles new web browser connections
    CONNECTED_BROWSERS.add(websocket) # registers only the newly connected browser
    print("---> Browser connected!")
    try:
        # keeps the connection handler alive without doing anything, waiting for the user to close their browser tab or refresh the page
        await websocket.wait_closed()
    finally:
        # guarantees that when the browser tab closes...
        CONNECTED_BROWSERS.remove(websocket) # .. this runs so we don't try sending data to dead connections
        print("<--- Browser disconnected")

async def main():
    # start local server on ws://localhost:8765 for the frontend
    async with websockets.serve(handle_browser, "localhost", 8765):
        # start listening to Binance continuously
        await binance_listener()

# Standard Python boiler-plate ensuring the script only executes when run directly
if __name__ == "__main__":
    asyncio.run(main())