import asyncio
from html.init_socketio import socketio

import requests
from db_work import SettingsManager
from flask import render_template


def render_settings_main_page():
    return render_template('settings/settings_main.html')


# Работа с токеном
@socketio.on('settingSetUpToken')
def get_token(data) -> None:
    flag: bool

    if token_valid(data):
        flag = True
    else:
        flag = False
    
    socketio.emit("settingTokenStatusPopup", flag)

    if flag:
        asyncio.run(SettingsManager().set_setting("bot.token", data))
    
    handle_check_token_status()

@socketio.on('settingCheckToken')
def handle_check_token_status():
    valid: bool
    
    token = asyncio.run(SettingsManager().get_setting("bot.token"))
    if token and token_valid(token):
        valid = True
    else:
        valid = False
    
    socketio.emit('settingTokenStatusUpdate', valid)

def token_valid(token: str) -> bool:
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': f'Bot {token}'})
        response.raise_for_status()

        return True
    
    except Exception:
        return False


# Работа с автозапуском
@socketio.on('settingSetUpAutoStart')
def get_auto_start(data) -> None:
    flag: bool
    
    try:
        asyncio.run(SettingsManager().set_setting("bot.auto_start", data))
        flag = True
    except Exception:
        flag = False
    
    socketio.emit("settingAutoStartStatusPopup", flag)
    handle_check_auto_start_status()

@socketio.on('settingCheckAutoStart')
def handle_check_auto_start_status():
    auto_start = asyncio.run(SettingsManager().get_setting("bot.auto_start"))
    socketio.emit('settingAutoStartStatusUpdate', auto_start)
