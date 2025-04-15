from pathlib import Path
import requests
from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import db, Category
import pymorphy3 as pymorphy2 

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456789012345678901234567890123456789'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"  
app.config['TELEGRAM_TOKEN'] = '7565599070:AAEwOj102OQanJq8liXBK1qZCrkKjcKld6w'
app.config["TELEGRAM_ADMIN_CHAT_ID"] = '1070122283'

db.init_app(app)

admin = Admin(app, name='My Admin', template_mode='bootstrap3')  

user_data = {}

def normalize_text(text):
    morph = pymorphy2.MorphAnalyzer()
    words = text.split()
    normalized_words = []

    for word in words:
        parsed_word = morph.parse(word)[0]
        normalized_words.append(parsed_word.normal_form)

    return ' '.join(normalized_words)

def categorize_message(data, keywords_list):
    normalized_message = normalize_text(data)
    max_keyword_count = 0
    category_id = None
    best_category_id = None
    print(normalized_message)

    for category_id, keywords in keywords_list.items():
        keyword_count = sum(1 for keyword in keywords if keyword in normalized_message)
        if keyword_count > max_keyword_count:
            max_keyword_count = keyword_count
            best_category_id = category_id

    return best_category_id

def send_message(chat_id, text, disable_notification=True):
    url = f"https://api.telegram.org/bot{app.config['TELEGRAM_TOKEN']}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "disable_notification": disable_notification
    }
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return {}

@app.route("/new_report", methods=["POST"])
def handle_new_report():
    data = request.get_json()
    print(f"\nПолучено новое сообщение: {data['text']}")  # Вывод полученного сообщения
    
    categories = Category.query.all()
    keywords = {category.name: [s.strip() for s in category.keywords.split(';')] for category in categories}
    
    print("Доступные категории и ключевые слова:")  # Вывод всех категорий для отладки
    for cat in categories:
        print(f"- {cat.name}: {cat.keywords}")
    
    category_name = categorize_message(data["text"], keywords)
    
    # Вывод определённой категории
    if category_name:
        print(f"Определена категория: {category_name}")
    else:
        print("Категория не определена")
    
    if category_name is None:
        send_message(app.config["TELEGRAM_ADMIN_CHAT_ID"], data["text"])
        return {"status": "warning", "message": "Категория не определена"}
    
    category = Category.query.filter_by(name=category_name).first()
    if category is None:
        return {"status": "error", "message": "Категория не найдена"}
    
    if category.default_answer is not None:
        print(f"Отправлен автоответ для категории {category_name}")
        return {"status": "default_answer", "answer": category.default_answer}
    
    chat_id = category.chat_id or app.config["TELEGRAM_ADMIN_CHAT_ID"]
    message = f"""Сообщение пользователя: {data["text"]}
Форма обратной связи: {data["callback"]}"""
    send_message(chat_id, message)
    print(f"Сообщение отправлено в чат категории {category_name} (ID: {chat_id})")
    return {"status": "send_to_telegram"}

def create_app():

    admin.add_view(ModelView(Category, db.session))
    with app.app_context():
        db.create_all()
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)