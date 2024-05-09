from telebot import types

def handle_teh(message, client):
    try:
        cid = message.message.chat.id
        uid = message.from_user.id
        msg = client.send_message(cid, f"*📨 | Enter the text you want to send to those support*", parse_mode='Markdown')
        client.register_next_step_handler(msg, handle_teh_next, client)
    except Exception as e:
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды для отправки сообщения в тех. поддержку: {e}')

def handle_teh_next(message, client):
	cid = message.chat.id
	uid = message.from_user.id

	try:
		if message.text == message.text:
			global tehtextbyuser
			global tehnamebyuser
			global tehidbyuser
			tehidbyuser = int(message.from_user.id)
			tehnamebyuser = str(message.from_user.first_name)
			tehtextbyuser = str(message.text)
			rmk = types.InlineKeyboardMarkup()
			item_yes = types.InlineKeyboardButton(text='✉️',callback_data='tehsend')
			item_no = types.InlineKeyboardButton(text='❌',callback_data='tehno')
			rmk.add(item_yes, item_no)
			msg = client.send_message(cid, f"✉️ | Information about the shipment:\n\n Text to send: {tehtextbyuser}\n\n Do you really want to send this to tech support?",parse_mode='Markdown',reply_markup=rmk)
	except:
		client.send_message(cid, f'🚫 | Ошибка при подтверждении отправки сообщения в тех. поддержку')

def handle_teh_callback(call, client, sql):
    try:
        if call.data == 'tehsend':
            # Fetch all users with access level 777
            users_with_access_777 = sql.execute("SELECT * FROM users WHERE access = 777").fetchall()
            
            # Iterate over each user and send the message
            for user in users_with_access_777:
                user_id = user[0]  # Assuming user ID is the first column in the table
                client.send_message(user_id, f"✉️ | Пользователь {call.from_user.id} отправил сообщение в тех.поддержку\n\nID пользователя: {call.from_user.id}\nТекст: {tehtextbyuser}\n\nЧтобы ответить пользователю напишите /ot")
            
            # Delete the message after sending it to all users
            client.delete_message(call.message.chat.id, call.message.message_id)
            
            # Send confirmation message to the user who initiated the action
            client.send_message(call.message.chat.id, f"✉️ | Your message has been sent to tech support, expect a response.")
        
        elif call.data == 'tehno':
            # Handle cancellation
            client.delete_message(call.message.chat.id, call.message.message_id)
            client.send_message(call.message.chat.id, f"🚫 | You canceled the sending of the tech message.support")
        
        client.answer_callback_query(callback_query_id=call.id)
    except Exception as e:
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при отправке сообщения в тех.поддержку: {e}')
