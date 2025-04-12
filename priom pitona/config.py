import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7565599070:AAEwOj102OQanJq8liXBK1qZCrkKjcKld6w")
ADMIN_CHAT_ID = os.getenv("1070122283")
EXCEL_FILE = os.getenv("EXCEL_FILE", "data/table.xlsx")
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://ваш_домен/webhook")
ADMIN_SECRET_KEY = os.getenv("ADMIN_SECRET_KEY", "1234")