from telebot import types
import sqlite3

def handle_sendmsgtouser(message, client, sql):
    cid = message.message.chat.id

    try:
        user_info = sql.execute(f"SELECT * FROM users WHERE id = {cid}").fetchone()
        
        if user_info:
            if user_info[3] == 777:
                msg = client.send_message(cid, f"👤 | Введите ID пользователя, которому хотите отправить сообщение:")
                client.register_next_step_handler(msg, handle_sendmsgtouser_next, client)
            else:
                msg = client.send_message(cid, f"👤 | Нет доступа")
        else:
            msg = client.send_message(cid, f"👤 | Нет информации о пользователе с ID {cid}")
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды отправки ID для сообщения пользователю: {e}')

def handle_sendmsgtouser_next(message, client):
    try:
        cid = message.chat.id
        getsendmsgtouserid = int(message.text)


        msg = client.send_message(cid, f"📨 | Введите текст, который хотите отправить пользователю:")
        client.register_next_step_handler(msg, handle_sendmsgtouser_next_text, client, getsendmsgtouserid)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды отправки сообщения пользователю: {e}')

# Импортируем необходимые модули
from telebot import types

# Создаем словарь для хранения текстовых сообщений
text_messages = {}

def handle_sendmsgtouser_next_text(message, client, user_id):
    try:
            getsendmsgtousertext = message.text
            
            client.delete_message(message.chat.id, message.message_id)
            client.send_message(message.chat.id, f"✉️ | Сообщение отправлено!")
            client.send_message(user_id, f"✉️ | Администратор прислал вам сообщение:\n\n{getsendmsgtousertext}")
            
    except Exception as e:
        client.send_message(message.chat.id, f'🚫 | Ошибка при отправке сообщения пользователю: {e}')
