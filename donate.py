
from telebot import types
import configure
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sqlite3


DONATE_MESSAGE = "*💰 | Введите сумму для пополнения:*"
ERROR_MESSAGE = "🚫 | Ошибка при выполнении команды для пополнения"
SUCCESSFUL_REQUEST_MESSAGE = "🔰 | Заявка на пополнение средств успешно создана\n\nВы действительно хотите пополнить средства?"

def handle_donate(message, client, sql):
    cid = message.message.chat.id

    try:
        client.delete_message(cid, message.message.message_id)

        msg = client.send_message(cid, DONATE_MESSAGE, parse_mode='Markdown')
        client.register_next_step_handler(msg, lambda message: handle_donate_value(message, client, sql, types))

    except:
        client.send_message(cid, ERROR_MESSAGE)

def handle_donate_value(message, client, sql, types):
    cid = message.chat.id

    try:
        uid = message.from_user.id
        if message.text == message.text:
            sql.execute(f"SELECT * FROM users WHERE id = {uid}")
            donatevalue = int(message.text)
            rmk = types.InlineKeyboardMarkup()
            item_yes = types.InlineKeyboardButton(text='✅', callback_data=f'donateyes_{donatevalue}')
            item_no = types.InlineKeyboardButton(text='❌', callback_data=f'donateno_{donatevalue}')

            rmk.add(item_yes, item_no)
            msg = client.send_message(cid, SUCCESSFUL_REQUEST_MESSAGE, parse_mode='Markdown', reply_markup=rmk)
    except:
        client.send_message(cid, ERROR_MESSAGE)

def handle_donateyes_paid(call, client, sql):
    try:
        uid = call.message.from_user.id
        cid = call.message.chat.id
        sql.execute("SELECT id FROM users WHERE access > 0")
        users_with_access = [row[0] for row in sql.fetchall()]
        print(call.data)

        if call.data.startswith('donatepaid'):
            donatevalue = call.data.split('_')[1]
            client.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем предыдущее сообщение

            for user_id in users_with_access:
                print(call.data)
                print(user_id)
                # Send the message to each user
                client.send_message(user_id, f"✉️ | Пользователь {uid} оплатил заявку на пополнение средств\n\n\nСумма: {donatevalue}$\n\nПерепроверьте верность оплаты затем подтвердите выдачу средств.\nДля выдачи средств напишите: /giverub")
            
            keyboard = [[types.InlineKeyboardButton('Меню', callback_data=f'help')]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            
            # Optionally, send a confirmation message to the original user
            client.send_message(cid, "✉️ | Ваш запрос отправлен администраторам, ожидайте одобрения и выдачи средств.", reply_markup=reply_markup)
    
    except Exception as e:
        error_message = f'🚫 | Ошибка: {e}'
        if cid is not None:
            client.send_message(cid, error_message)
        else:
            print(error_message)

            
def handle_donate_result(call, client, sql):
    crypto_wallet = configure.config['crypto_wallet']
    try:
        if call.data.startswith('donateyes_'):
            donatevalue = call.data.split('_')[1]
            client.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем предыдущее сообщение
            
            # Creating the reply markup with the "Оплачено" button
            keyboard = [[types.InlineKeyboardButton('✅ Оплачено', callback_data=f'donatepaid_{donatevalue}')]]
            reply_markup = types.InlineKeyboardMarkup(keyboard)
            
            # Sending the message with the correct reply markup
            client.send_message(call.message.chat.id, f"➖➖➖➖➖➖➖➖➖➖➖➖\n☎️ Кошелек для оплаты: {crypto_wallet}\n💰 Сумма: {donatevalue}$\n➖➖➖➖➖➖➖➖➖➖➖➖", parse_mode='Markdown', reply_markup=reply_markup)
            return donatevalue
            
        elif call.data.startswith('donateno_'):
            client.answer_callback_query(callback_query_id=call.id)
            client.send_message(call.message.chat.id, "❌ | Вы отменили заявку на пополнение средств")
    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при выполнении команды получения результата оплаты: {str(e)}')
