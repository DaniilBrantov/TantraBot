import configure

def handle_allusers(message, sql, client):
    try:
        cid = message.chat.id
        uid = message.from_user.id

        # Получаем уровень доступа пользователя
        sql.execute("SELECT access FROM users WHERE id = ?", (uid,))
        user_access = sql.fetchone()[0]

        # Проверяем уровень доступа пользователя
        accessquery = 1
        if user_access < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            # Формируем список всех пользователей
            text = '*🗃 | Список всех пользователей:*\n\n'
            idusernumber = 0
            for info in sql.execute("SELECT * FROM users"):
                accessname = ""
                if info[3] == 0:
                    accessname = 'Пользователь'
                elif info[3] == 1:
                    accessname = 'Администратор'
                elif info[3] == 777:
                    accessname = 'Разработчик'
                idusernumber += 1
                text += f"*{idusernumber}. {info[0]} ({info[1]})*\n*💸 | Баланс:* {info[2]} ₽\n*👑 | Уровень доступа:* {accessname}\n*✉️ | Профиль:*" + f" [{info[1]}](tg://user?id="+str(info[0])+")\n\n"
            
            # Отправляем сообщение со списком пользователей
            client.send_message(cid, f"{text}",parse_mode='Markdown')
    except Exception as e:
        # Если возникает ошибка, сообщаем об этом пользователю
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды вывода всех пользователе: {str(e)}')

def handle_getprofile(message, sql, client):
    cid = message.message.chat.id

    try:
        uid = message.from_user.id

        # Получаем уровень доступа пользователя
        sql.execute("SELECT access FROM users WHERE id = ?", (uid,))
        user_access = sql.fetchone()[0]

        # Проверяем уровень доступа пользователя
        accessquery = 1
        if user_access < accessquery:
            client.send_message(cid, '⚠️ | У вас нет доступа!')
        else:
            for info in sql.execute(f"SELECT * FROM users WHERE id = {uid}"):
                msg = client.send_message(cid, f'Введите ID пользователя:\nПример: {info[0]}')
                client.register_next_step_handler(msg, handle_getprofile_next, sql, client)
    except Exception as e:
        # Если возникает ошибка, сообщаем об этом пользователю
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды получения информации о профиле: {str(e)}')

def handle_getprofile_next(message, sql, client):
    try:
        cid = message.chat.id
        uid = message.from_user.id
        getprofileid = int(message.text)

        # Получаем информацию о профиле целевого пользователя
        for info in sql.execute(f"SELECT * FROM users WHERE id = {getprofileid}"):
            accessname = ""
            if info[3] == 0:
                accessname = 'Пользователь'
            elif info[3] == 1:
                accessname = 'Администратор'
            elif info[3] == 777:
                accessname = 'Разработчик'
            client.send_message(cid, f"*📇 | Профиль {info[1]}:*\n\n*ID пользователя:* {info[0]}\n*Баланс:* {info[2]} ₽\n*Уровень доступа:* {accessname}\n*Куплено товаров:* {info[4]}", parse_mode='Markdown')
    except Exception as e:
        # Если возникает ошибка, сообщаем об этом пользователю
        client.send_message(cid, f'🚫 | Ошибка при выполнении команды получения информации о профиле пользователя: {str(e)}')

def handle_getrazrabotchik(message, sql, client, db):
    try:
        admin_id = configure.config['admin_id']
        if message.from_user.id == int(admin_id):
            sql.execute(f"UPDATE users SET access = 777 WHERE id = ?", (admin_id,))
            db.commit()
            client.send_message(message.chat.id, f"✅ | Вы выдали себе Разработчика")
        else:
            client.send_message(message.chat.id, f"⛔️ | Отказано в доступе!")
            print(message.from_user.id)
    except Exception as e:
        client.send_message(message.chat.id, f'🚫 | Ошибка: {e}')
