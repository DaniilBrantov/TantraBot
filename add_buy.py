from telebot import types

def handle_addbuy(call, client, lock, sql, db):
    cid = call.message.chat.id
    uid = call.from_user.id
    try:
        with lock:
            sql.execute(f"SELECT * FROM users WHERE id = {uid}")
            getaccess = sql.fetchone()

        if getaccess is None:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            getaccess = getaccess[3]  # Получаем третий элемент кортежа (индекс 3)
            if getaccess < 1:
                client.send_message(cid, '⚠️ | У вас нет доступа!')
            else:
                # Добавляем кнопку "Назад" к сообщению о запросе изображения услуги
                keyboard = types.InlineKeyboardMarkup()
                callback_button = types.InlineKeyboardButton(text="Назад", callback_data="help")
                keyboard.add(callback_button)
                
                # Отправляем сообщение о запросе изображения услуги с кнопкой "Назад"
                message_text = 'Отправьте изображение услуги:\n'   # Adding a unique identifier
                msg = client.send_message(cid, message_text, reply_markup=keyboard)
                
                # Регистрируем обработчик следующего шага
                client.register_next_step_handler(msg, handle_addbuy_image, client, sql, db)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды добавления услуги: {e}')

def handle_addbuy_image(message, client, sql, db):
    cid = message.chat.id
    uid = message.from_user.id
    try:


        # Проверяем, является ли сообщение изображением
        if message.photo:
            # Удаляем предыдущее сообщение
            client.delete_message(cid, message.message_id)

            # Получаем file_id фото
            photo_file_id = message.photo[-1].file_id
            # client.send_message(cid, 'Теперь введите ID, цену, название и описание услуги через запятую:')

            # Добавляем кнопку "Назад"
            keyboard = types.InlineKeyboardMarkup()
            callback_button = types.InlineKeyboardButton(text="Назад", callback_data="help")
            keyboard.add(callback_button)

            # Отправляем новое сообщение с запросом ввода информации об услуге и кнопкой "Назад"
            msg = client.send_message(cid, 'Теперь введите ID / цену / Название / описание услуги через "/".\n( 1/999/Название/Ваше описание ): ', reply_markup=keyboard)
            client.register_next_step_handler(msg, handle_addbuy_process, photo_file_id, client, sql, db)
        else:
            client.send_message(cid, '⚠️ | Пожалуйста, отправьте изображение услуги.')
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды добавления изображения: {e}')
     
def handle_addbuy_process(message, photo_file_id, client, sql, db):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        data = message.text.split('/')
        addbuyid, addbuyprice, addbuyname, addbuydescription = data[:4]
        
        # Выполнение SQL-запроса для добавления нового услуги в таблицу shop
        sql.execute("INSERT INTO shop (id, price, name, image, description) VALUES (?, ?, ?, ?, ?);",
                    (addbuyid, addbuyprice, addbuyname, photo_file_id, addbuydescription))
        db.commit()  # Фиксация изменений в базе данных

        response = f'''✅ Товар успешно добавлен!

        ID услуги: {addbuyid}
        Название: {addbuyname}
        Цена: {addbuyprice}
        Описание: {addbuydescription}
        '''
        client.send_message(cid, response)
        # Отправляем фото
        client.send_photo(cid, photo_file_id, caption="Изображение услуги")

    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды добавления услуги: {e}')
