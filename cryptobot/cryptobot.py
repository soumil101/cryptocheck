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

# class MyWebsocketClient(cbpro.WebsocketClient):
#     def on_open(self):
#         self.url = "wss://ws-feed.pro.coinbase.com/"
#         self.products = ["BTC-USD"]
#         self.message_count = 0
#         print("Websocket Client started")

#     def on_message(self, msg):
#         if 'price' in msg and 'type' in msg:
#             print(f"Received {msg['type']} message for {msg['product_id']}: {msg['price']}")

#     def on_close(self):
#         print("Websocket Client closed")

# wsClient = MyWebsocketClient()
# wsClient.start()

# def on_open(ws):
#     print("opened")
#     subscribe_message = {
#         "type": "subscribe",
#         "channels": [
#             {
#                 "name": "ticker",
#                 "product_ids": [
#                     "BTC-USD",
#                     "ETH-USD",
#                     "ETH-EUR"
#                 ]
#             }
#         ]
#     }
#     ws.send(json.dumps(subscribe_message))

# def on_close(ws):
#     print("closed connection")

# def on_message(ws, message):
#     print(message)

# socket = "wss://ws-feed.pro.coinbase.com"
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_close=on_close, on_message=on_message)
# ws.run_forever()

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
        print(message)

    def start(self):
        self.ws.run_forever()

trading_pairs = ["BTC-USD"]
wsClient = CoinbaseProWebsocketClient(trading_pairs)
wsClient.start() 
