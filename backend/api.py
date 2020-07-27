
import websocket
import json
import time

global json_data

ws = websocket.WebSocket()
ws.connect('ws://localhost:8000/ws/polData')
for i in range(100):
    time.sleep(1)
    ws.send(json.dumps({"value":"g"}))

    