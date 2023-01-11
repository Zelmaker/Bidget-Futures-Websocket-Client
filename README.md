# Bitget Futures Websocket Client

This is a python script for connecting to the Bitget Futures websocket and subscribe to the orders channel, also the script will send a message to Telegram if the server goes down.

## Requirements
- Python 3.7+
- websockets library
- requests library
- asyncio library
- json library

## Usage
- Replace the following in the script with your own Bitget API key and secret, and Telegram token and channel_id:
```python
    apiKey = 'your_api_key'
    passphrase = 'your_passphrase'
    secretKey = 'your_secret_key'
    telegram_token = "your_telegram_token"
    telegram_channel_id = "your_telegram_channel_id"
