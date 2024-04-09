import requests
from telegram import KeyboardButton, ReplyKeyboardMarkup

TOKEN = "6319183234:AAGZW-pv7ENjuYTpKFdngw39ICNX1z6Dpl4"
BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"


button1 = KeyboardButton('/location')
button2 = KeyboardButton('/contact')
button3 = KeyboardButton('/aboutme')
custom_keyboard = [[button1], [button2], [button3]]
reply_markup = ReplyKeyboardMarkup(custom_keyboard)


def make_request(method: str, params: dict = None):
    res = requests.get(f"{BASE_URL}{method}", params=params)
    return res.json()

def get_updates(offset: int = 0):
    return make_request("getUpdates", {"offset": offset})["result"]


def send_contact(chat_id):
    make_request(
        "sendContact",
        {
            "chat_id": chat_id,
            "phone_number": "+998-99-919-40-33",
            "first_name": "Ravshanjon",
            "text": "This is my personal contact number which you can use for contacting me bro)",
            "phone_number":"88 342 4033",
            "required": True
        }
    )


def send_location(chat_id):
    make_request(
        "sendLocation",
        {
            "chat_id": chat_id,
            "latitude": 41.3018004,
            "longitude": 69.2263596
        }
    )

def send_about_me(chat_id):
    make_request(
        "sendPhoto",
        {
            "chat_id": chat_id,
            "photo": "https://www.dropbox.com/scl/fi/dj3qai29vkzphx294mkjk/1.jpg?rlkey=yrk48vxguduz1qjhb4dhn769t&dl=0",
        }
    )
    make_request(
        "sendPhoto",
        {
            "chat_id": chat_id,
            "photo": "https://www.dropbox.com/scl/fi/rjrbt6r50er9ppi1gxhx7/2.jpg?rlkey=wlq8eq93avsdoortzu28cg73e&dl=0",
            "caption": "My name is Ravshanjon, I am senior developer at UIC company"
        }
    )

def other_message(chat_id):
    make_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Use special commands or use /help if you want to interact with bot"
        }
    )

def start(chat_id):
    make_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Choose an option:",
            "reply_markup": reply_markup.to_json()
        }
    )

def help(chat_id):
    commands = [
        "/start - Start the bot",
        "/help - Show available commands",
        "/location - Share Ravshanjon's location",
        "/contact - Share your contact information",
        "/aboutme - My bio"
    ]
    commands_text = "\n".join(commands)
    make_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Available commands:\n" + commands_text
        }
    )

def button(chat_id):
    make_request(
        "sendMessage",
        {
            "chat_id": chat_id,
            "text": "Choose button: ",
            "reply_markup": reply_markup.to_json()
        }
    )

def main():
    offset = 0
    while True:
        updates = get_updates(offset)
        for update in updates:
            offset = update["update_id"] + 1
            if "message" in update and "text" in update["message"]:
                text = update["message"]["text"]
                chat_id = update["message"]["chat"]["id"]
                if text == '/button':
                    button(chat_id)
                elif text == '/contact':
                    send_contact(chat_id)
                elif text == '/location':
                    send_location(chat_id)
                elif text == '/aboutme':
                    send_about_me(chat_id)
                elif text == '/start':
                    start(chat_id)
                elif text == '/help':
                    help(chat_id)
                else:
                    other_message(chat_id)


if __name__ == "__main__":
    main()