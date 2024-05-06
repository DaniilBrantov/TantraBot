import telebot
from telebot import types
import sqlite3

def handle_helpcmd(call, client, lock, sql):
    cid = call.message.chat.id
    uid = call.from_user.id
    with lock:
        # Устанавливаем row_factory для корректной работы с именами столбцов
        sql.row_factory = sqlite3.Row
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        row = sql.fetchone()
    if row:
        # Если результат запроса не пустой
        if isinstance(row, sqlite3.Row):
            # Если результат запроса - это объект sqlite3.Row
            getaccess = row['access']
            balance = row['balance']

            # Создаем инлайн-клавиатуру
            keyboard = types.InlineKeyboardMarkup()

            # Добавляем кнопки для общих команд
            # keyboard.add(types.InlineKeyboardButton("Профиль 👤", callback_data='profile'))
            keyboard.add(types.InlineKeyboardButton("Услуги 💸", callback_data='buy'))
            keyboard.add(types.InlineKeyboardButton("Написать мне 📞", callback_data='teh'))

            # Если у пользователя уровень доступа 1 или выше, добавляем команды администратора
            if isinstance(getaccess, int):
                if getaccess >= 1:
                    # keyboard.add(types.InlineKeyboardButton("Посмотреть чужой профиль", callback_data='getprofile'))
                    # keyboard.add(types.InlineKeyboardButton("Узнать айди пользователя", callback_data='getid'))
                    keyboard.add(types.InlineKeyboardButton("Добавить товар на продажу", callback_data='addbuy'))
                    keyboard.add(types.InlineKeyboardButton("Изменить данные об услуге", callback_data='editbuy'))
                    keyboard.add(types.InlineKeyboardButton("Удалить товар", callback_data='rembuy'))
                    keyboard.add(types.InlineKeyboardButton("Ответить пользователю", callback_data='ot'))

            # Отправляем сообщение с инлайн-клавиатурой
            client.edit_message_text(chat_id=cid, message_id=call.message.message_id, text='*Помощь по командам:*\n\nНажмите на кнопку, чтобы выполнить команду', parse_mode='Markdown', reply_markup=keyboard)
        else:
            # Если результат запроса не является объектом sqlite3.Row
            client.send_message(cid, "Ошибка: неверный формат данных в базе данных")
    else:
        # Если результат запроса пустой
        client.send_message(cid, "Ошибка: пользователь не найден в базе данных")
