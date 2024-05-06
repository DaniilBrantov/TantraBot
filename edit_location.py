from telebot import types

def handle_editbuy(message, client, sql, lock):
    try:
        cid = message.message.chat.id
        uid = message.from_user.id
        accessquery = 1
        with lock:
            sql.execute(f"SELECT * FROM users WHERE id = {uid}")
            getaccess = sql.fetchone()[3]
        if getaccess < 1:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            rmk = types.InlineKeyboardMarkup()
            item_name = types.InlineKeyboardButton(text='Название',callback_data='editbuyname')
            item_price = types.InlineKeyboardButton(text='Цена',callback_data='editbuyprice')
            item_tovar = types.InlineKeyboardButton(text='Товар',callback_data='editbuytovar')
            item_image = types.InlineKeyboardButton(text='Изображение',callback_data='editbuyimage')
            item_description = types.InlineKeyboardButton(text='Описание',callback_data='editbuydescription')
            rmk.add(item_name, item_price, item_tovar, item_image, item_description)
            msg = client.send_message(cid, f"🔰 | Выберите что Вы хотите изменить:",reply_markup=rmk,parse_mode='Markdown')
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды изменения услуги: {e}')

def handle_editbuy_name(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuynameidtovar
            editbuynameidtovar = int(message.text)
            msg = client.send_message(cid, f"*Введите новое название услуги:*", parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_name_new_name, client, sql)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды изменения названия: {e}')

def handle_editbuy_name_new_name(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuynametovar
            editbuynametovar = message.text
            for infoshop in sql.execute(f"SELECT * FROM shop WHERE id = {editbuynameidtovar}"):
                rmk = types.InlineKeyboardMarkup()
                item_yes = types.InlineKeyboardButton(text='✅', callback_data='editbuynewnametovaryes')
                item_no = types.InlineKeyboardButton(text='❌', callback_data='editbuynewnametovarno')
                rmk.add(item_yes, item_no)
                msg = client.send_message(cid, f"*🔰 | Данные об изменении названия услуги:*\n\nID услуги: {editbuynameidtovar}\nСтарое имя услуги: {infoshop[1]}\nНовое имя услуги: {editbuynametovar}\n\nВы подверждаете изменения?", parse_mode='Markdown', reply_markup=rmk)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при сохранении нового названия: {e}')

def handle_editbuy_price(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuypriceidtovar
            editbuypriceidtovar = int(message.text)
            msg = client.send_message(cid, f"*Введите новую цену услуги:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_price_new_price, client, sql)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды измения цены: {e}')

def handle_editbuy_price_new_price(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuypricetovar
            editbuypricetovar = int(message.text)
            for infoshop in sql.execute(f"SELECT * FROM shop WHERE id = {editbuypriceidtovar}"):
                rmk = types.InlineKeyboardMarkup()
                item_yes = types.InlineKeyboardButton(text='✅', callback_data='editbuynewpricetovaryes')
                item_no = types.InlineKeyboardButton(text='❌', callback_data='editbuynewpricetovarno')
                rmk.add(item_yes, item_no)
                msg = client.send_message(cid, f"*🔰 | Данные об изменении цены услуги:*\n\nID услуги: {editbuypriceidtovar}\nСтарая цена: {infoshop[2]}\nНовая цена: {editbuypricetovar}\n\nВы подверждаете изменения?",parse_mode='Markdown',reply_markup=rmk)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при сохранении цены услуги : {e}')

def handle_editbuy_tovar(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuytovaridtovar
            editbuytovaridtovar = int(message.text)
            msg = client.send_message(cid, f"*Введите новую ссылку на услугу:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_tovar_new_tovar, client, sql)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды изменения ссылки: {e}')

def handle_editbuy_tovar_new_tovar(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuytovartovar
            editbuytovartovar = message.text
            for infoshop in sql.execute(f"SELECT * FROM shop WHERE id = {editbuytovaridtovar}"):
                rmk = types.InlineKeyboardMarkup()
                item_yes = types.InlineKeyboardButton(text='✅', callback_data='editbuynewtovartovaryes')
                item_no = types.InlineKeyboardButton(text='❌', callback_data='editbuynewtovartovarno')
                rmk.add(item_yes, item_no)
                msg = client.send_message(cid, f"*🔰 | Данные об изменении сcылки услуги:*\n\nID услуги: {editbuytovaridtovar}\nСтарая ссылка: {infoshop[3]}\nНовая ссылка: {editbuytovartovar}\n\nВы подверждаете изменения?",parse_mode='Markdown',reply_markup=rmk)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при сохранении новой ссылки: {e}')

def handle_editbuy_image(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text.isdigit():
            global editbuyimageidtovar
            editbuyimageidtovar = int(message.text)
            msg = client.send_message(cid, f"Пришлите новое изображение:", parse_mode='Markdown')
            client.register_next_step_handler_by_chat_id(cid, handle_editbuy_image_new_image, client, sql)
        else:
            client.send_message(cid, f'⚠️ | Введите ID услуги в числовом формате.')
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды изменения изображения: {e}')

def handle_editbuy_image_new_image(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.photo:  # Проверяем, содержит ли сообщение изображение
            file_id = message.photo[-1].file_id  # Получаем file_id последнего изображения в сообщении
            global editbuyimagetovar
            editbuyimagetovar = file_id
            for infoshop in sql.execute(f"SELECT image FROM shop WHERE id = {editbuyimageidtovar}"):
                rmk = types.InlineKeyboardMarkup()
                item_yes = types.InlineKeyboardButton(text='✅', callback_data='editbuynewimagetovaryes')
                item_no = types.InlineKeyboardButton(text='❌', callback_data='editbuynewimagetovarno')
                rmk.add(item_yes, item_no)
                # Экранируем подчеркивания в тексте
                if infoshop[0] is not None:  # Проверяем, что значение столбца image не пустое
                    client.send_photo(cid, infoshop[0], caption="Старое изображение", parse_mode='Markdown')
                else:
                    client.send_message(cid, "Старое изображение: Не имеется")

                caption_text = f"🔰 | Данные об изменении изображения услуги:\n\nID услуги: {editbuyimageidtovar}\nНовое изображение: 👆👆\n\nВы подтверждаете изменения?"
                client.send_photo(cid, file_id, caption=caption_text, parse_mode='Markdown', reply_markup=rmk)
                
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при сохранении изображения: {e}')


def handle_editbuy_description(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text.isdigit():
            global editbuydescriptionidtovar
            editbuydescriptionidtovar = int(message.text)
            msg = client.send_message(cid, "Введите новое описание услуги:")
            client.register_next_step_handler(msg, handle_editbuy_description_new_description, client, sql)
        else:
            client.send_message(cid, '⚠️ | Введите ID услуги в числовом формате.')
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды изменения описания: {e}')

def handle_editbuy_description_new_description(message, client, sql):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        if message.text == message.text:
            global editbuydescriptiontovar
            editbuydescriptiontovar = message.text
            for infoshop in sql.execute(f"SELECT description FROM shop WHERE id = {editbuydescriptionidtovar}"):
                rmk = types.InlineKeyboardMarkup()
                item_yes = types.InlineKeyboardButton(text='✅', callback_data='editbuynewdescriptiontovaryes')
                item_no = types.InlineKeyboardButton(text='❌', callback_data='editbuynewdescriptiontovarno')
                rmk.add(item_yes, item_no)
                msg = client.send_message(cid, f"🔰 | Данные об изменении описания услуги:\n\nID услуги: {editbuydescriptionidtovar}\nСтарое описание: {infoshop[0]}\nНовое описание: {editbuydescriptiontovar}\n\nВы подтверждаете изменения?", reply_markup=rmk)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при сохранении описания: {e}')



def handle_editbuy_tovar_new_callback(call, client, sql, db):
    try:
        if call.data == 'editbuynewtovartovaryes':
            sql.execute(f"SELECT * FROM shop WHERE id = {editbuytovaridtovar}")
            sql.execute(f"UPDATE shop SET tovar = '{editbuytovartovar}' WHERE id = {editbuytovaridtovar}")
            db.commit()
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"✅ | Вы успешно изменили ссылку на услугу на {editbuytovartovar}")
        elif call.data == 'editbuynewtovartovarno':
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили изменение сcылки услуги")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при сохранении новой ссылки услуги')

def handle_editbuy_price_new_callback(call, client, sql, db):
    try:
        if call.data == 'editbuynewpricetovaryes':
            sql.execute(f"SELECT * FROM shop WHERE id = {editbuypriceidtovar}")
            sql.execute(f"UPDATE shop SET price = {editbuypricetovar} WHERE id = {editbuypriceidtovar}")
            db.commit()
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"✅ | Вы успешно изменили цену услуги на {editbuypricetovar}")
        elif call.data == 'editbuynewpricetovarno':
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили изменение цены услуги")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при сохранении новой цены услуги')

def handle_editbuy_name_new_callback(call, client, sql, db):
    try:
        if call.data == 'editbuynewnametovaryes':
            sql.execute(f"SELECT * FROM shop WHERE id = {editbuynameidtovar}")
            sql.execute(f"UPDATE shop SET name = '{editbuynametovar}' WHERE id = {editbuynameidtovar}")
            db.commit()
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"✅ | Вы успешно изменили название услуги на {editbuynametovar}")
        elif call.data == 'editbuynewnametovarno':
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили изменение названия услуги")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при выполнении команды изменения названия')

def handle_editbuy_first_callback(call, client, sql):
    try:
        if call.data == 'editbuyname':
            msg = client.send_message(call.message.chat.id, f"*Введите ID услуги которому хотите изменить название:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_name, client, sql)
        elif call.data == 'editbuyprice':
            msg = client.send_message(call.message.chat.id, f"*Введите ID услуги которому хотите изменить цену:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_price, client, sql)
        elif call.data == 'editbuytovar':
            msg = client.send_message(call.message.chat.id, f"*Введите ID услуги которому хотите изменить ссылку:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_tovar, client, sql)
        elif call.data == 'editbuyimage':
            msg = client.send_message(call.message.chat.id, f"*Введите ID услуги которому хотите изменить картинку:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_image, client, sql)
        elif call.data == 'editbuydescription':
            msg = client.send_message(call.message.chat.id, f"*Введите ID услуги которому хотите изменить описание:*",parse_mode='Markdown')
            client.register_next_step_handler(msg, handle_editbuy_description, client, sql)
        
        client.answer_callback_query(callback_query_id=call.id)
        
    except:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при выполнении команды для изменения услуги')

def handle_editbuy_image_new_callback(call, client, sql, db):
    try:
        if call.data == 'editbuynewimagetovaryes':
            sql.execute(f"SELECT * FROM shop WHERE id = {editbuyimageidtovar}")
            sql.execute(f"UPDATE shop SET image = '{editbuyimagetovar}' WHERE id = {editbuyimageidtovar}")
            db.commit()
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_photo(call.message.chat.id, editbuyimagetovar, caption=f"✅ | Вы успешно изменили изображение услуги", parse_mode='Markdown')
        elif call.data == 'editbuynewimagetovarno':
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили изменение изображения услуги")
        client.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при выполнении команды изменения изображения: {e}')


def handle_editbuy_description_new_callback(call, client, sql, db):
    try:
        if call.data == 'editbuynewdescriptiontovaryes':
            sql.execute(f"SELECT * FROM shop WHERE id = {editbuydescriptionidtovar}")
            sql.execute(f"UPDATE shop SET description = '{editbuydescriptiontovar}' WHERE id = {editbuydescriptionidtovar}")
            db.commit()
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"✅ | Вы успешно изменили описание услуги на {editbuydescriptiontovar}")
        elif call.data == 'editbuynewdescriptiontovarno':
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили изменение описания услуги")
        client.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при выполнении команды изменения описания: {e}')