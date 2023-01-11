import asyncio
import json
import requests
import websockets
import time
import base64
import hmac
import hashlib

PING_MESSAGE = 'ping'
PONG_MESSAGE = 'pong'

# Replace these with your Bitget API key and secret
apiKey = 'your_api_key'
passphrase = 'your_passphrase'
secretKey = 'your_secret_key'
# Replace these with your Telegram keys
telegram_token = "your_telegram_token"
telegram_channel_id = "your_telegram_channel_id"


def send_telegram(text: str):
    token = "telegram_token"
    url = "https://api.telegram.org/bot"
    channel_id = "telegram_channel_id"
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
        "chat_id": channel_id,
        "text": text
    })

    if r.status_code != 200:
        raise Exception("post_text error")


def send_ping(websocket):
    asyncio.get_event_loop().create_task(websocket.send(PING_MESSAGE))
    print('send ping')


async def connect():
    uri = "wss://ws.bitget.com/mix/v1/stream"
    async with websockets.connect(uri) as websocket:
        timestamp = str(int(time.time()))
        content = timestamp + 'GET' + '/user/verify'
        hash = hmac.new(bytes(secretKey, 'utf-8'), bytes(content, 'utf-8'), hashlib.sha256).digest()
        signature = base64.b64encode(hash).decode('utf-8')
        auth_request = {
            "op": "login",
            "args": [
                {
                    "apiKey": apiKey,
                    "passphrase": passphrase,
                    "timestamp": timestamp,
                    "sign": signature
                }
            ]
        }
        await websocket.send(json.dumps(auth_request))
        auth_response = json.loads(await websocket.recv())
        print(auth_response)
        if auth_response["code"] != 0:
            print(f"Authentication error code: {auth_response['code']}")
        else:
            # Subscribe to the orders channel
            orders_request = {
                "op": "subscribe",
                "args": [{
                    "channel": "orders",
                    "instType": "UMCBL",
                    "instId": "default"
                }]
            }
            await websocket.send(json.dumps(orders_request))
            order_response = json.loads(await websocket.recv())
            print(order_response)
            timer = asyncio.get_event_loop().call_later(30, send_ping, websocket)
            message = None
            while True:
                try:
                    message = await websocket.recv()
                except json.JSONDecodeError:
                    print(f'some json decoding error {message}')

                # If the message is a pong, reset the timer
                if message == PONG_MESSAGE:
                    timer.cancel()
                    timer = asyncio.get_event_loop().call_later(30, send_ping, websocket)
                else:
                    message_data = json.loads(message)
                    if message_data.get('action') == 'snapshot':
                        coin = message_data.get("data")[0].get("instId").replace("_UMCBL", "")
                        posside = message_data.get("data")[0].get("posSide")  # long/short
                        side = message_data.get("data")[0].get("side")  # buy/sell
                        quantity = message_data.get("data")[0].get("sz")
                        amountusdt = message_data.get("data")[0].get("notionalUsd")
                        ordtype = message_data.get("data")[0].get("ordType")  # market/limit
                        tdmode = message_data.get("data")[0].get("tdMode")  # cross/fixed
                        if message_data.get("data")[0].get("status") == 'new':
                            send_telegram(
                                f'NEW Order: Coin {coin}, side: {posside} | {side}, quantity: {quantity},amountusdt: {amountusdt},ordtype: {ordtype},tdmode: {tdmode}')
                        elif message_data.get("data")[0].get("status") == 'cancelled':
                            send_telegram(
                                f'Canceled Order: Coin {coin}, side: {posside} | {side}, quantity: {quantity},amountusdt: {amountusdt},ordtype: {ordtype},tdmode: {tdmode}')
                        # elif message_data.get("data")[0].get("status") == 'full-fill':
                        #     print(f'Filled Order: Coin {message_data.get("data")[0].get("instId")}, side: {message_data.get("data")[0].get("posSide")}, ordertype: {message_data.get("data")[0].get("ordType")}, USDT on order: {message_data.get("data")[0].get("notionalUsd")}')


asyncio.get_event_loop().run_until_complete(connect())
