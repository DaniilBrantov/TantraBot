from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

WELCOME_TEXT = "🛒 | Welcome, {name}!"
HELP_TEXT = "Hello and welcome!\n\n Contact our operators for payment assistance!"
ERROR_TEXT = '🚫 | Error executing the start command: {error}'
HELP_BUTTON_TEXT = "👉 Get what I need 👈"

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
    help_button = InlineKeyboardButton(HELP_BUTTON_TEXT, callback_data='help')
    markup.add(help_button)
    return markup
