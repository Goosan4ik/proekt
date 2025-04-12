import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = '7565599070:AAEwOj102OQanJq8liXBK1qZCrkKjcKld6w'

ADMIN_CHAT_ID = '1070122283'

user_data = {}

def send_message(chat_id, text, disable_notification=True):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "disable_notification": disable_notification
    }
    response = requests.post(url, json=data)
    return response.json()

@app.route("/new_report", methods=["POST"])

def new_report():
    data = request.get_json()
    msg=f"""Сообщение пользователя: {data["text"]}
Форма обратной связи: {data["callback"]}"""
    send_message(1070122283, msg)
    return {"status": "ok"}

if __name__ == "__main__":
    app.run(debug=True,port=5000)