from telebot import types

def handle_removebuy(message, client, sql, lock):
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
			msg = client.send_message(cid, f"*Введите ID услуги который хотите удалить:*",parse_mode='Markdown')
			client.register_next_step_handler(msg, handle_removebuy_next, client, sql)
	except:
		client.send_message(cid, f'🚫 | Ошибка при выполнении команды выбора ID для удаления услуги')

def handle_removebuy_next(message, client, sql):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if message.text == message.text:
			global removeidtovar
			removeidtovar = int(message.text)
			for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
				for infoshop in sql.execute(f"SELECT * FROM shop WHERE id = {removeidtovar}"):
					rmk = types.InlineKeyboardMarkup()
					item_yes = types.InlineKeyboardButton(text='✅',callback_data='removebuytovaryes')
					item_no = types.InlineKeyboardButton(text='❌',callback_data='removebuytovarno')
					rmk.add(item_yes, item_no)
					msg = client.send_message(cid, f"🔰 | Данные об удалении:\n\nID услуги: {infoshop[0]}\nИмя услуги: {infoshop[1]}\nЦена услуги: {infoshop[2]}\nТовар: {infoshop[3]}\n\nВы действительно хотите удалить товар? Отменить действие будет НЕВОЗМОЖНО.",reply_markup=rmk)
	except:
		client.send_message(cid, f'🚫 | Ошибка удалении услуги')


def handle_removebuy_callback(call, client, sql, db):
    try:
        if call.data == 'removebuytovaryes':
            # Удаление услуги из базы данных
            sql.execute(f"DELETE FROM shop WHERE id = {removeidtovar}")
            db.commit()
            # Уведомление об успешном удалении услуги
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"✅ | Вы успешно удалили товар")
        elif call.data == 'removebuytovarno':
            # Отмена удаления услуги
            client.delete_message(call.message.chat.id, call.message.message_id-0)
            client.send_message(call.message.chat.id, f"🚫 | Вы отменили удаление услуги")
        client.answer_callback_query(callback_query_id=call.id)
    except:
        # Обработка ошибок при выполнении команды
        client.send_message(call.message.chat.id, f'🚫 | Ошибка при удалении услуги')
