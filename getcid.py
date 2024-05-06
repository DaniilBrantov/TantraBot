def handle_getcid(message,client):
	client.send_message(message.message.chat.id, f"ID чата | {message.message.chat.id}\nТвой ID | {message.from_user.id}")
