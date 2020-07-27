
import websocket
import json
import time

import random

global json_data

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/souhard')
for i in range(100):
    time.sleep(3)
    ws.send(json.dumps({"value":random.randint(1,100)}))

    