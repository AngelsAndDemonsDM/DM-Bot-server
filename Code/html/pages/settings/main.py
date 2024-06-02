import asyncio
from html.init_socketio import socketio

import requests
from bot import bot, main
from flask import render_template


def render_settings_main_page():
    return render_template('settings/settings_main.html')

# Нам прислали токен, пируем (обрабатываем)
@socketio.on('sendToken')
def get_token(data):
    anser: str
    flag: bool

    if token_valid(data):
        anser = "Токен принят"
        flag = True
    else:
        anser = "Токен не верный"
        flag = False
    
    socketio.emit("anserFromPy", anser)

    if flag:
        file_work = 123(TOKEN_PATH)

        file_work.data = data
        file_work.save_data()
        is_has_token()

# Проверка того, что токен валидный
def token_valid(token: str) -> bool:
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': f'Bot {token}'}) # Немного магии
        
        if response.status_code == 200:
            return True

        return False
    
    except Exception: # В случае если ошибка любая - токен какашка, не кушаем!
        return False

# У нас запросили наличие токена
@socketio.on('isHasToken')
def is_has_token():
    file_work = 123(TOKEN_PATH)
    try:
        file_work.load_data()
    
        if file_work.data is None:
            socketio.emit("getIsHasToken", False)
        else:
            socketio.emit("getIsHasToken", True)
    except Exception:
        socketio.emit("getIsHasToken", False)

@socketio.on('startBot')
def start_bot():
    try:
        asyncio.run(main())
    except Exception:
        socketio.emit("anserFromPy", "Токен <p class=\"red\"style=\"display: inline;\">не обнаружен</p>")

# Отправка статуса бота
@socketio.on('requestBotStatus')
def send_bot_status():
    socketio.emit("getBotStatus", bot.is_ready())
