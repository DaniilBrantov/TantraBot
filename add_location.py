from telebot import types
import sqlite3
from telegram.ext import CallbackQueryHandler

def check_access(uid, sql, lock):
    try:
        with lock:
            sql.execute("SELECT access FROM users WHERE id = ?", (uid,))
            access_level = sql.fetchone()
            if access_level and access_level[0] >= 1:
                return True
        return False
    except Exception as e:
        print(f"Ошибка при проверке доступа: {e}")
        return False

def handle_send_district_choice_message(message, client, sql, lock):
    try:
        cid = message.message.chat.id
        if not check_access(cid, sql, lock):
            client.send_message(cid, '⚠️ | У вас нет доступа!')
            return
        

        rmk = types.InlineKeyboardMarkup()
        sql.execute("SELECT id, district FROM district")
        sql.row_factory = sqlite3.Row  # Установка row_factory
        districts = sql.fetchall()
        for row in districts:
            district_id = row['id']
            district_name = row['district']
            callback_data = f"addproductlocation_{district_id}"
            button = types.InlineKeyboardButton(text=district_name, callback_data=callback_data)
            rmk.add(button)
        
        client.send_message(cid, '🔰 | Выберите район, в который хотите добавить продукт:', reply_markup=rmk)
        
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при отправке сообщения: {e}')


def handle_productlocation_callback(call, client, sql):
    cid = call.message.chat.id

    try:
        selected_district = call.data.split('_')[1]

        sql.row_factory = sqlite3.Row

        sql.execute("SELECT * FROM shop")
        products = sql.fetchall()

        rmk = types.InlineKeyboardMarkup()
        for product in products:
            product_name = product['name']
            callback_data = f"addlocphoto_{product['id']}_{selected_district}"
            button = types.InlineKeyboardButton(text=product_name, callback_data=callback_data)
            rmk.add(button)

        client.send_message(cid, 'Выберите продукт:', reply_markup=rmk)
        
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при обработке выбора локации: {e}')

def handle_addloc_photo(call, client, sql, db):
    try:
        cid = call.message.chat.id
        product_id = call.data.split('_')[1]
        district_id = call.data.split('_')[2]

        # Отправляем запрос на отправку общего изображения локации
        client.send_message(cid, 'Отправьте общее изображение локации:')
        
        # Сохраняем информацию о выбранном продукте и районе в словаре для этого чата
        if not hasattr(client, 'user_data'):
            client.user_data = {}
        client.user_data[cid] = {'product_id': product_id, 'district_id': district_id}

        # Регистрируем следующий шаг обработчика для получения изображения
        client.register_next_step_handler(call.message, handle_general_location_photo, client, sql, db)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при отправке сообщения: {e}')

def handle_general_location_photo(message, client, sql, db):
    try:
        cid = message.chat.id

        # Проверяем, что пришло фото
        if message.photo:
            # Получаем file_id последнего отправленного фото
            general_photo = message.photo[-1].file_id

            # Получаем информацию о продукте и районе из user_data
            user_data = client.user_data.get(cid, {})
            product_id = user_data.get('product_id', '')
            district_id = user_data.get('district_id', '')

            # Отправляем запрос на отправку более детального изображения локации
            client.send_message(cid, 'Теперь отправьте более детальное изображение локации:')

            # Сохраняем file_id общего изображения в user_data
            user_data['general_photo'] = general_photo
            client.user_data[cid] = user_data

            # Регистрируем следующий шаг обработчика для получения более детального изображения
            client.register_next_step_handler(message, handle_detailed_location_photo, client, sql, db)
        else:
            client.send_message(cid, '⚠️ | Пожалуйста, отправьте изображение локации.')
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при обработке изображения: {e}')

def handle_detailed_location_photo(message, client, sql, db):
    try:
        cid = message.chat.id

        # Проверяем, что пришло фото
        if message.photo:
            # Получаем file_id последнего отправленного фото
            detailed_photo = message.photo[-1].file_id

            # Получаем информацию о продукте, районе и общем изображении из user_data
            user_data = client.user_data.get(cid, {})
            product_id = user_data.get('product_id', '')
            district_id = user_data.get('district_id', '')
            general_photo = user_data.get('general_photo', '')

            # Отправляем запрос на ввод локации
            client.send_message(cid, 'Отлично! Теперь введите локацию:')

            # Сохраняем file_id более детального изображения в user_data
            user_data['detailed_photo'] = detailed_photo
            client.user_data[cid] = user_data

            # Регистрируем следующий шаг обработчика для получения локации
            client.register_next_step_handler(message, handle_location_input, client, sql, db, product_id, district_id, general_photo, detailed_photo)
        else:
            client.send_message(cid, '⚠️ | Пожалуйста, отправьте более детальное изображение.')
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при обработке изображения: {e}')

def handle_location_input(message, client, sql, db, product_id, district_id, general_photo, detailed_photo):
    try:
        cid = message.chat.id
        location = message.text

        # Преобразование product_id и district_id в int
        product_id = int(product_id)
        district_id = int(district_id)

        # Начать транзакцию
        with db:
            # Вставить данные в базу данных
            sql.execute("INSERT INTO locations (district_id, product_id, location, image, detailed_image) VALUES (?, ?, ?, ?, ?)",
                        (district_id, product_id, location, general_photo, detailed_photo))
            db.commit() 

        # Получить имя продукта и района из базы данных
        with db:
            sql.row_factory = sqlite3.Row
            cursor = db.cursor()
            cursor.execute("SELECT name FROM shop WHERE id=?", (product_id,))
            product_name = cursor.fetchone()[0]  # Правильный способ получения значения из кортежа

            cursor.execute("SELECT district FROM district WHERE id=?", (district_id,))
            district_name = cursor.fetchone()[0]  # Правильный способ получения значения из кортежа

        # Отправить сообщение об успешном добавлении локации
        response = f'''✅ Локация успешно добавлена!

        Район: {district_name}
        Товар: {product_name}
        Локация: {location}
        '''
        client.send_message(cid, response)
        client.send_photo(cid, general_photo, caption="Общая фотография локации")
        client.send_photo(cid, detailed_photo, caption="Более детальная фотография локации")
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды добавления локации: {e}')
