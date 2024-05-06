from telebot import types
def handle_givemoney(message, sql, client):
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
				msg = client.send_message(cid, 'Введите ID пользователя:\nПример: 522567233', parse_mode="Markdown")
				client.register_next_step_handler(msg, handle_money_user_id_answer,client, sql)
	except:
		client.send_message(cid, f'🚫 | Ошибка при выполнении команды для выдачи денег пользователю')

def handle_money_user_id_answer(message, client, sql):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if message.text == message.text:
			global usridmoney
			usridmoney = message.text
			rmk = types.ReplyKeyboardMarkup(resize_keyboard=True)
			rmk.add(types.KeyboardButton('10'), types.KeyboardButton('100'), types.KeyboardButton('1000'), types.KeyboardButton('Другая сумма'))
			msg = client.send_message(cid, 'Выберите сумму для выдачи:', reply_markup=rmk, parse_mode="Markdown")
			client.register_next_step_handler(msg, handle_money_user_money_answer, client, sql)
	except:
		client.send_message(cid, f'🚫 | Ошибка при выполнении команды выбора суммы для выдачи')

def handle_money_user_money_answer(message, client, sql):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		global moneygavedvalue
		removekeyboard = types.ReplyKeyboardRemove()
		rmk = types.InlineKeyboardMarkup()
		access_yes = types.InlineKeyboardButton(text='✅',callback_data='givemoneyyes')
		access_no = types.InlineKeyboardButton(text='❌',callback_data='givemoneyno')
		rmk.add(access_yes, access_no)
		for info in sql.execute(f"SELECT * FROM users WHERE id = {usridmoney}"):
			if message.text == '10':
				moneygavedvalue = 10
				client.send_message(cid, f'Данные для выдачи:\nID пользователя: {usridmoney} ({info[1]})\nСумма: {moneygavedvalue}\n\nВерно?',reply_markup=rmk)
			elif message.text == '100':
				moneygavedvalue = 100
				client.send_message(cid, f'Данные для выдачи:\nID пользователя: {usridmoney} ({info[1]})\nСумма: {moneygavedvalue}\n\nВерно?',reply_markup=rmk)
			elif message.text == '1000':
				moneygavedvalue = 1000
				client.send_message(cid, f'Данные для выдачи:\nID пользователя: {usridmoney} ({info[1]})\nСумма: {moneygavedvalue}\n\nВерно?',reply_markup=rmk)
			elif message.text == 'Другая сумма':
				msg = client.send_message(cid, f"*Введите сумму для выдачи:*",parse_mode='Markdown',reply_markup=removekeyboard)
				client.register_next_step_handler(msg, handle_money_user_money_answer_other, client, sql)
	except:
		client.send_message(cid, f'🚫 | Ошибка при выполнении команды для выдачи предложенной суммы денег пользователю')

def handle_money_user_money_answer_other(message, client, sql):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		global moneygavedvalue
		rmk = types.InlineKeyboardMarkup()
		access_yes = types.InlineKeyboardButton(text='✅',callback_data='givemoneyyes')
		access_no = types.InlineKeyboardButton(text='❌',callback_data='givemoneyno')
		rmk.add(access_yes, access_no)
		for info in sql.execute(f"SELECT * FROM users WHERE id = {usridmoney}"):
			if message.text == message.text:
				moneygavedvalue = int(message.text)
				client.send_message(cid, f'Данные для выдачи:\nID пользователя: {usridmoney} ({info[1]})\nСумма: {moneygavedvalue}\n\nВерно?',reply_markup=rmk)
	except:
		client.send_message(cid, f'🚫 |  Ошибка при выполнении команды для выдачи конкретной суммы денег пользователю')


def handle_money_gave_money_user(call, client, sql, db):
	try:
		removekeyboard = types.ReplyKeyboardRemove()
		for info in sql.execute(f"SELECT * FROM users WHERE id = {usridmoney}"): 
			moneys = int(info[2] + moneygavedvalue)
			if call.data == 'givemoneyyes':
				for info in sql.execute(f"SELECT * FROM users WHERE id = {usridmoney}"):
					sql.execute(f"UPDATE users SET balance = {moneys} WHERE id = {usridmoney}")
					db.commit()
					client.delete_message(call.message.chat.id, call.message.message_id-0)
					client.send_message(call.message.chat.id, f'✅ | Пользователю {info[1]} выдано {moneygavedvalue} рублей', reply_markup=removekeyboard)
			elif call.data == 'givemoneyno':
				for info in sql.execute(f"SELECT * FROM users WHERE id = {usridmoney}"):
					client.delete_message(call.message.chat.id, call.message.message_id-0)
					client.send_message(call.message.chat.id, f'🚫 | Вы отменили выдачу рублей пользователю {info[1]}', reply_markup=removekeyboard)
			client.answer_callback_query(callback_query_id=call.id)
	except:
		client.send_message(call.message.chat.id, f'🚫 |  Ошибка при выдаче денег пользователю')
