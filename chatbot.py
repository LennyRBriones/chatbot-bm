import openai
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

Token = os.getenv("BOT_TOKEN")

openai.api_key = os.getenv("API_KEY_OPENAI")

def get_updates(offsets):
    url = f"https://api.telegram.org/bot{Token}/getUpdates"
    params = {"timeout": 100, "offset": offsets}
    response = requests.get(url, params=params)
    return response.json()["result"]

def send_messages(chat_id, text):
    url = f"https://api.telegram.org/bot{Token}/sendMessage"
    params = {"chat_id": chat_id, "text": text}
    response = requests.post(url, params=params)
    return response

def get_openai_response(prompt):
    model_engine = os.getenv("MODEL_ENGINE")
    response = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens = 70,
        n = 1,
        stop=["END"],
        temperature=0.01,
        best_of=2,
        frequency_penalty=1,
        top_p=0,
        presence_penalty=0
        
        

    )
    return response.choices[0].text.strip()

def main():
    print("Starting bot...")
    offset = 0
    while True:
        updates = get_updates(offset)
        if updates:
            for update in updates:
                offset = update["update_id"] + 1
                chat_id = update["message"] ["chat"]["id"]
                user_message = update["message"]["text"]
                print(f"Receive messeage: {user_message}")
                GPT = get_openai_response(user_message)
                send_messages(chat_id, GPT)
        else:
             time.sleep(1)

if __name__ == "__main__":
    main()
