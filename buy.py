import telebot
from telebot import types
import configure

# Список ID администраторов (должен быть заранее задан)
ADMIN_ID = configure.config['admin_id']

# Обработчик вывода всех товаров
def handle_buy(message, client, sql):
    try:
        cid = message.chat.id
        # Получаем все товары из базы данных
        all_products = sql.execute("SELECT * FROM shop").fetchall()

        if not all_products:
            client.send_message(cid, "🛒 | The list of items is empty.")
            return

        for product in all_products:
            product_id = product[0]
            product_name = product[1]
            product_price = product[2]
            product_description = product[4]
            product_photo = product[3]

            # Создаем описание товара
            text = f"{product_name}\n{product_description}\nPrice: {product_price} Rp.\n\n"

            # Создаем кнопки "Купить"
            rmk = types.InlineKeyboardMarkup()
            item_buy = types.InlineKeyboardButton(text='Buy', callback_data=f'confirm_order_{product_id}')
            rmk.add(item_buy)

            # Отправляем сообщение пользователю
            if product_photo:
                client.send_photo(
                    cid,
                    photo=product_photo,
                    caption=text,
                    parse_mode='Markdown',
                    reply_markup=rmk
                )
            else:
                client.send_message(
                    cid,
                    text,
                    parse_mode='Markdown',
                    reply_markup=rmk
                )

    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при получении списка товаров: {e}')


# Обработчик подтверждения заказа
def handle_confirm_order(call, client, sql):
    try:
        message_id = call.message.message_id
        # Получаем ID товара из callback_data
        product_id = int(call.data.split('_')[2])

        # Получаем информацию о товаре
        product = sql.execute(f"SELECT * FROM shop WHERE id = {product_id}").fetchone()

        if product:
            product_name = product[1]
            product_price = product[2]
            product_description = product[4]
            product_photo = product[3]

            # Создаем описание товара
            text = (
                f"You want to buy the following item:\n\n"
                f"Name: {product_name}\n"
                f"Description: {product_description}\n"
                f"Price: {product_price} rubles\n\n"
                f"Are you sure you want to buy?"
            )

            # Создаем кнопки подтверждения
            rmk = types.InlineKeyboardMarkup()
            confirm_button = types.InlineKeyboardButton(text='Yes', callback_data=f'order_confirmed_{product_id}')
            cancel_button = types.InlineKeyboardButton(text='No', callback_data=f'order_confirmed_0')
            rmk.add(confirm_button, cancel_button)

            # Редактируем сообщение с новой информацией
            if product_photo:
                client.edit_message_media(
                    chat_id=call.message.chat.id,
                    message_id=message_id,
                    media=telebot.types.InputMediaPhoto(
                        media=product_photo,
                        caption=text,
                        parse_mode='Markdown'
                    ),
                    reply_markup=rmk
                )
            else:
                client.edit_message_text(
                    text=text,
                    chat_id=call.message.chat.id,
                    message_id=message_id,
                    parse_mode='Markdown',
                    reply_markup=rmk
                )

    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при подтверждении заказа: {e}')


def handle_order_confirmation(call, client, sql):
    try:
        # Разбиваем callback_data на части
        data_parts = call.data.split('_')

        # Убедимся, что список имеет хотя бы 3 элемента
        if len(data_parts) < 3:
            raise ValueError("Недостаточно данных в callback_data")

        product_id = int(data_parts[2])

        if product_id < 1:
            # Проверяем, есть ли 4-й элемент в списке (идентификатор сообщения)
            if len(data_parts) > 3:
                # Удаляем предыдущее сообщение, если информация о нем есть
                message_id = int(data_parts[3])
                client.delete_message(call.message.chat.id, message_id)
                # Создаем кнопки подтверждения
            

            rmk = types.InlineKeyboardMarkup()
            menu_button = types.InlineKeyboardButton(text='Menu', callback_data=f'help')
            rmk.add(menu_button)
            client.send_message(call.message.chat.id, "❌ | The order has been cancelled.", reply_markup=rmk)

        elif product_id > 0:
            # Сообщаем пользователю об успешном подтверждении
            client.delete_message(call.message.chat.id, call.message.message_id-0)

            user_id = call.from_user.id
            user_link = f"tg://user?id={user_id}"
            rmk = types.InlineKeyboardMarkup()
            menu_button = types.InlineKeyboardButton(text='Menu', callback_data=f'help')
            rmk.add(menu_button)
            client.send_message(call.message.chat.id, "✅ | The order has been confirmed. Your order will be processed and we will contact you", reply_markup=rmk
            )

            # Отправляем сообщение администраторам
            client.send_message(ADMIN_ID, f"⚠️ | Новый заказ подтвержден:\nID услуги: {product_id}\nID пользователя: {user_id}\n Ссылка на аккаунт: {user_link}")

        # Подтверждаем, что обработали callback
        client.answer_callback_query(call.id)

    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при обработке подтверждения заказа: {e}')
