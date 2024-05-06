def handle_getiduser(message, client, sql):
	try:
		cid = message.message.chat.id
		uid = message.from_user.id
		sql.execute(f"SELECT * FROM users WHERE id = {uid}")
		getaccess = sql.fetchone()[3]
		accessquery = 1
		if getaccess < accessquery:
			client.send_message(cid, f"⚠️ | У вас нет доступа!")
		else:
			msg = client.send_message(cid, 'Введите никнейм пользователя:')
			client.register_next_step_handler(msg, handle_next_getiduser_name, client, sql)
	except:
		client.send_message(cid, f'🚫 | Ошибка при выполнении команды для получения информации о пользователе')

def handle_next_getiduser_name(message, client, sql):
	try:
		cid = message.chat.id
		uid = message.from_user.id
		if message.text == message.text:
			getusername = message.text
			sql.execute(f"SELECT * FROM users WHERE nick = '{getusername}'")
			result = sql.fetchone()[0]
			client.send_message(cid, f'👤 | ID пользователя: {result}')
	except:
		client.send_message(cid, f'🚫 | Ошибка при выполнении команды для вывода информации о пользователе')
