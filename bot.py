import telebot
import threading
import configure
from database import initialize_database, sql, db


# Инициализация базы данных
initialize_database()

# Создание объекта блокировки
lock = threading.Lock()

# Инициализация клиента Telebot
client = telebot.TeleBot(configure.config['token'])

from start import handle_start
from admin import handle_getrazrabotchik
from callbacks import *

# Регистрация обработчика команды /start
@client.message_handler(commands=['start'])
def start(message):
            
    admin_id = configure.config['admin_id']  # Assuming user ID is the first column in the table
    client.send_message(admin_id, f"✉️ | Пользователь {message.from_user.id} начал пользоваться ботом\n\nID пользователя: {message.from_user.id}\n\nЧтобы написать пользователю напишите /ot")
            
    handle_start(message, sql, db, client)

@client.message_handler(commands=['get_admin'])
def get_admin(message):
    handle_getrazrabotchik(message, sql, client, db)

# @client.message_handler(commands=['help'])
# def get_admin(message):
#     handle_helpcmd(message, sql, client, db)

@client.message_handler(commands=['ot'])
def ot(message):
    handle_sendmsgtouser(message, client, sql)


# Регистрация всех обработчиков колбэков
@client.callback_query_handler(func=lambda call: True)
def handle_query(call):
    callback_type = call.data.split('_')[0]
    if callback_type in callbacks:
        callbacks[callback_type](call, client, sql, db)

# Запуск бота
client.polling(none_stop=True, interval=0)
