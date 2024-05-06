from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

WELCOME_TEXT = "🛒 | Добро пожаловать, {name}!"
HELP_TEXT = "Привет и добро пожаловать! ✌️ \n\n Для оплаты покупки обращайтесь к нашим операторам!"
ERROR_TEXT = '🚫 | Ошибка при выполнении команды start: {error}'
HELP_BUTTON_TEXT = "👉 Получить то,что мне нужно 👈"

def handle_start(message, sql, db, client):
    cid = message.chat.id
    uid = message.from_user.id
    try:
        getname = message.from_user.first_name

        sql.execute(f"SELECT id FROM users WHERE id = {uid}")
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES ({uid}, '{getname}', 0, 0, 0)")
            client.send_message(cid, WELCOME_TEXT.format(name=getname), reply_markup=create_help_button())
            db.commit()
        else:
            client.send_message(cid, HELP_TEXT, reply_markup=create_help_button())
    except Exception as e:
        client.send_message(cid, ERROR_TEXT.format(error=str(e)))

def create_help_button():
    markup = InlineKeyboardMarkup()
    help_button = InlineKeyboardButton(HELP_BUTTON_TEXT, callback_data='buy')
    markup.add(help_button)
    return markup
