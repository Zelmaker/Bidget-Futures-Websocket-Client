# Bitget Futures Websocket Client

This is a python script for connecting to the Bitget Futures websocket and subscribe to the orders channel, also the script will send a message to Telegram when new orders placed

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
```
- Run the script using the command:
python bitget_websocket.py
- you should see the authenticated successfully on the console

## Telegram Alert
- If server goes down, the script can't run, to get notified of the server going down, you can use different cloud-based monitoring service or a cron job that regularly pings your server to check its availability, and sends a message to Telegram if it doesn't get a response.

## Notes
- Please make sure you are in compliance with Bitget's terms of service and API policies.
- Handle the errors in script, and also the invalid response from the telegram api and retry sending message after certain interval in case of any failure.
- The script is for educational purposes and should not be used in production without proper testing and modification.

## Resources
- Bitget Futures Websocket API documentation: [link](https://docs.bitget.com/)
- Telegram API documentation: [link](https://core.telegram.org/bots/api)

## Author
[Zelmaker](https://github.com/Zelmaker)
