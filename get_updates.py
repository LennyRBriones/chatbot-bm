import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("BOT_TOKEN")


def get_updates(token, offset=None):
    url = f"https://api.telegram.org/bot{token}/getUpdates"
    params = {'offset': offset} if offset else {}
    response = requests.get(url, params=params)
    return response.json()


def print_new_messages(token):
    offset = None
    while True:
        updates = get_updates(token, offset)
        if "result" in updates:
            for update in updates["result"]:
                message = update["message"]
                id = message["from"]["id"]
                username = message["from"]["first_name"]
                text = message.get("text")
                print(f"Usuario: {username} ({id})")
                print(f"Mensaje: {text}")
                print("---")
                # get the following updates 1 by 1
                offset = update["update_id"] + 1
        time.sleep(1)  # waits 1 second before get new updates


print_new_messages(token)
