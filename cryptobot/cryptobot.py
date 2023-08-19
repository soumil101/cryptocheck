import cbpro
import websocket
import json
import time

import os
from dotenv import load_dotenv

load_dotenv()

# fetch coinbase pro api key and passphrase
COINBASE_PRO_PUBLIC_KEY = os.getenv('COINBASE_PRO_PUBLIC_KEY')
COINBASE_PRO_API_KEY = os.getenv('COINBASE_PRO_API_SECRET')
COINBASE_PRO_PASSPHRASE = os.getenv('COINBASE_PRO_PASSPHRASE')

# create authenticated client
auth = cbpro.AuthenticatedClient(COINBASE_PRO_PUBLIC_KEY, COINBASE_PRO_API_KEY, COINBASE_PRO_PASSPHRASE)

class CoinbaseProWebsocketClient:
    def __init__(self, trading_pairs):
        self.trading_pairs = trading_pairs
        self.socket = "wss://ws-feed.pro.coinbase.com"
        self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)

    def on_open(self, ws):
        print("WebSocket connection established. Subscribing to ticker feed...")
        subscribe_message = {
            "type": "subscribe",
            "channels": [
                {
                    "name": "ticker",
                    "product_ids": self.trading_pairs
                }
            ]
        }
        ws.send(json.dumps(subscribe_message))

    def on_close(self, ws):
        print("WebSocket connection closed. Reconnecting...")
        time.sleep(5)
        self.start()

    def on_message(self, ws, message):
        ticker = json.loads(message)
        if 'price' in ticker:
            print(f"Latest BTC-USD price: {ticker['price']}")

    def start(self):
        while True:
            try:
                self.ws = websocket.WebSocketApp(self.socket, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
                self.ws.run_forever()
            except websocket.WebSocketException as e:
                print(f"WebSocket error: {e}")
                self.ws.close()
                time.sleep(5)

trading_pairs = ["BTC-USD"]
wsClient = CoinbaseProWebsocketClient(trading_pairs)
wsClient.start() 
