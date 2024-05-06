from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def handle_myprofile(call, sql, client):
    cid = call.message.chat.id

    try:
        uid = call.from_user.id

        # Получаем информацию о пользователе из базы данных
        sql.execute("SELECT * FROM users WHERE id = ?", (uid,))
        user_data = sql.fetchone()

        if user_data:
            # Определяем уровень доступа пользователя
            access = user_data[3]
            if access == 0:
                accessname = 'Пользователь'
            elif access == 1:
                accessname = 'Администратор'
            elif access == 777:
                accessname = 'Разработчик'

            # Формируем информацию о профиле пользователя
            profile_info = f"*📇 | Твой профиль:*\n\n*👤 | Ваш ID:* {user_data[0]}\n*💸 | Баланс:* {user_data[2]} ₽\n*👑 | Уровень доступа:* {accessname}\n*🛒 | Куплено товаров:* {user_data[4]}\n\n"
            
            # Создаем клавиатуру с кнопками "Купленные товары" и "Назад" в столбик
            my_buy_button = InlineKeyboardButton("Купленные товары", callback_data='mybuy')
            back_button = InlineKeyboardButton("Назад", callback_data='help')
            keyboard = InlineKeyboardMarkup().add(my_buy_button, back_button)

            # Редактируем предыдущее сообщение пользователя
            client.edit_message_text(chat_id=cid, message_id=call.message.message_id, text=profile_info, parse_mode='Markdown', reply_markup=keyboard)
        else:
            # Если пользователь не найден в базе данных
            client.send_message(cid, f"⛔️ | Ты не зарегистрирован в системе. Пропиши /start для регистрации.")
    except Exception as e:
        # Если возникает ошибка, сообщаем об этом пользователю
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды Профиля: {str(e)}')
