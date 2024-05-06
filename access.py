from telebot import types

def handle_setaccess(message, client, sql, db):
    cid = message.message.chat.id
    try:
        uid = message.from_user.id
        sql.execute(f"SELECT * FROM users WHERE id = {uid}")
        getaccess = sql.fetchone()[3]
        accessquery = 777
        if getaccess < accessquery:
            client.send_message(cid, f"⚠️ | У вас нет доступа!")
        else:
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                msg = client.send_message(cid, 'Введите ID пользователя:\nПример: 669456298', parse_mode="Markdown")
                client.register_next_step_handler(msg, handle_access_user_id_answer, client, sql, db)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды access')

def handle_access_user_id_answer(message, client, sql, db):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
            rmk.add(types.KeyboardButton('Пользователь'), types.KeyboardButton('Администратор'), types.KeyboardButton('Разработчик'))
            msg = client.send_message(cid, 'Какой уровень доступа Вы хотите выдать?:', reply_markup=rmk, parse_mode="Markdown")
            client.register_next_step_handler(msg, handle_access_user_access_answer, client, sql, db)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды access')

def handle_access_user_access_answer(message, client, sql, db):
    try:
        global accessgaved
        global accessgavedname
        cid = message.chat.id
        uid = message.from_user.id
        rmk = types.InlineKeyboardMarkup()
        access_yes = types.InlineKeyboardButton(text='✅',callback_data='setaccessyes')
        access_no = types.InlineKeyboardButton(text='❌',callback_data='setaccessno')
        rmk.add(access_yes, access_no)
        for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
            if message.text == "Пользователь":
                accessgavedname = "Пользователь"
                accessgaved = 0
            elif message.text == "Администратор":
                accessgavedname = "Администратор"
                accessgaved = 1
            elif message.text == "Разработчик":
                accessgavedname = "Разработчик"
                accessgaved = 777

            client.send_message(cid, f'Данные для выдачи:\nID пользователя: {uid} ({info[1]})\nУровень доступа: {message.text}\n\nВерно?', reply_markup=rmk)
    except:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды access')

def handle_access_user_gave_access(call, client, sql, db):
    cid = call.message.chat.id
    uid = call.from_user.id
    try:
        removekeyboard = types.ReplyKeyboardRemove()
        if call.data == 'setaccessyes':
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                sql.execute(f"UPDATE users SET access = {accessgaved} WHERE id = {uid}")
                db.commit()
                client.delete_message(call.message.chat.id, call.message.message_id-0)
                client.send_message(call.message.chat.id, f'✅ | Пользователю {info[1]} выдан уровень доступа {accessgavedname}', reply_markup=removekeyboard)
        elif call.data == 'setaccessno':
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                client.delete_message(call.message.chat.id, call.message.message_id-0)
                client.send_message(call.message.chat.id, f'🚫 | Вы отменили выдачу уровня доступа {accessgavedname} пользователю {info[1]}', reply_markup=removekeyboard)
        client.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды access: {e}')
