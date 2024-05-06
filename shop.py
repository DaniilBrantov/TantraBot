import telebot
from telebot import types

def handle_mybuy(message, sql, client):
    cid = message.message.chat.id
    mid = message.message.message_id  # Получаем ID предыдущего сообщения
    
    try:
        uid = message.from_user.id
        
        # Формируем список купленных товаров текущего пользователя
        text = '*🗂 | Список купленных товаров:*\n\n'
        has_items = False  # Флаг, чтобы отслеживать наличие купленных товаров
        for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
            if info is not None:  # Проверяем, что информация о пользователе получена
                for infoshop in sql.execute("SELECT * FROM shop"):
                    if infoshop[6] is not None and str(info[0]) in infoshop[6]:
                        text += f"*{infoshop[1]}*\n"
                        has_items = True
        
        # Если пользователь не купил ни одного услуги, добавляем сообщение "пусто"
        if not has_items:
            text += "У вас нет купленных товаров\n"
        
        # Удаляем предыдущее сообщение
        client.delete_message(cid, mid)
        
        # Добавляем кнопку "Назад"
        keyboard = types.InlineKeyboardMarkup()
        callback_button = types.InlineKeyboardButton(text="Назад", callback_data="profile")
        keyboard.add(callback_button)
        
        # Отправляем сообщение с списком купленных товаров
        client.send_message(cid, f"{text}", parse_mode='Markdown', reply_markup=keyboard, disable_web_page_preview=True)
        
        
    except Exception as e:
        # Если возникает ошибка, сообщаем об этом пользователю
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды для получения списка купленных товаров: {str(e)}')
