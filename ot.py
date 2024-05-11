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

def handle_sendmsgtouser_next_text(message, client, user_id):
    cid = message.chat.id

    try:
        getsendmsgtousertext = message.text
        rmk = types.InlineKeyboardMarkup()
        item_yes = types.InlineKeyboardButton(text='✅', callback_data=f'sendmsgtouseryes_{user_id}_{getsendmsgtousertext}')  # передаем текст через callback_data
        item_no = types.InlineKeyboardButton(text='❌', callback_data='sendmsgtouserno')
        rmk.add(item_yes, item_no)
        msg = client.send_message(cid, f"🔰 | Данные об отправке сообщения:\n\nID пользователя: {user_id}\nТекст для отправки: {getsendmsgtousertext}\n\nОтправить сообщение?", reply_markup=rmk)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды подтверждения отправки сообщения пользователю: {e}')

def handle_sendmsgtouser_callback(call, client, sql):
    print("Callback data:", call.data)
    
    try:
        
        # Извлекаем текст из callback_data
        user_id = call.data.split('_')[1]
        getsendmsgtousertext = call.data.split('_')[2]
        if call.data.startswith('sendmsgtouseryes'):
            client.delete_message(call.message.chat.id, call.message.message_id)
            client.send_message(call.message.chat.id, f"✉️ | Сообщение отправлено!")
            client.send_message(user_id, f"✉️ | Администратор прислал вам сообщение:\n\n{getsendmsgtousertext}")
        elif call.data == 'sendmsgtouserno':
            client.delete_message(call.message.chat.id, call.message.message_id)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили отправку сообщения пользователю")
        client.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при отправке сообщения пользователю: {e}')
