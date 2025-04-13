import requests
from flask import Flask, request
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import pymorphy2


app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
admin = Admin()

TOKEN = '7565599070:AAEwOj102OQanJq8liXBK1qZCrkKjcKld6w'

ADMIN_CHAT_ID = '1070122283'

user_data = {}

category1_path = r'\data\lichni_kabinet.txt'
category2_path = r'\data\lichnie_dannie.txt'
category3_path = r'\data\naim_zhilogo_pomeshenia.txt'
category4_path = r'\data\nevernoe_otobrazhenie.txt'
category5_path = r'\data\oplata_obychenia.txt'
category6_path = r'\data\problemi_s_saitom.txt'
category7_path = r'\data\spravki.txt'
category8_path = r'\data\vibornie_disciplini.txt'
category9_path = r'\data\ytochnenie_informacii.txt'
category10_path = r'\data\zadolzhennosti.txt'


def load_words_from_file(file_path):
    return []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            words = text.split()
        return words
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return []


keywords1 = load_words_from_file(category1_path)
keywords2 = load_words_from_file(category2_path)
keywords3 = load_words_from_file(category3_path)
keywords4 = load_words_from_file(category4_path)
keywords5 = load_words_from_file(category5_path)
keywords6 = load_words_from_file(category6_path)
keywords7 = load_words_from_file(category7_path)
keywords8 = load_words_from_file(category8_path)
keywords9 = load_words_from_file(category9_path)
keywords10 = load_words_from_file(category10_path)

keywords_list = [keywords1, keywords2, keywords3, keywords4, keywords5, 
                 keywords6, keywords7, keywords8, keywords9, keywords10]

def normalize_text(text):
    morph = pymorphy2.MorphAnalyzer()
    words = text.split()
    normalized_words = []

    for word in words:
        parsed_word = morph.parse(word)[0]
        normalized_words.append(parsed_word.normal_form)

    return ' '.join(normalized_words)

def category_identificator(data, keywords_list):
    print(keywords_list)
    message = normalize_text(data)
    maxcount = 0
    flag = 0
    category = ''
    
    for index, keywords in keywords_list.items():
        count = sum(1 for keyword in keywords if keyword in message)
        if count > maxcount:
            maxcount = count
            flag = index

    category_map = {
        1: 'личный кабинет',
        2: 'личные данные',
        3: 'найм жилого помещения',
        4: 'неверное отображение',
        5: 'оплата обучения',
        6: 'проблемы с сайтом',
        7: 'справки',
        8: 'выборные дисциплины',
        9: 'уточнение информации',
        10: 'задолженности'
    }

    return flag

def send_message(chat_id, text, disable_notification=True):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
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
def new_report():
    from models import db, Category
    from collections import defaultdict
    data = request.get_json()
    with app.app_context():
        # categories = db.session.Query(Category).all()
        categories = db.session.execute(db.select(Category)).all()
    keywords = defaultdict(list)
    for cat in categories[0]:
        print(cat)
        keywords[cat.name].extend(cat.keywords.split(';'))
    flag =  category_identificator(data["text"], keywords)
    print(flag)
    # with app.app_context():
        # category = db.session.execute(db.select(Category).filter_by(name=flag)).all()[0]
    category = categories[flag]
    print(category)
    if category.default_answer is not None:
        return {"status": "default_answer", "answer": default_answer}
    chat_id = ADMIN_CHAT_ID if category.chat_id is None else category.chat_id
    msg = f"""Сообщение пользователя: {data["text"]}
Форма обратной связи: {data["callback"]}"""
    send_message(chat_id, msg)
    return {"status": "ok"}

def create_app():
    from models import db, Category
    db.init_app(app)
    admin.init_app(app)
    with app.app_context():
        db.create_all()
    admin.add_view(ModelView(Category, db.session))
    return app

if __name__ == "__main__":
    create_app().run(debug=True, port=5000)


