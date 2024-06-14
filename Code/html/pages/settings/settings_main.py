import asyncio
from html.init_socketio import socketio

import requests
from db_work import SettingsManager
from flask import render_template


def render_settings_main_page():
    return render_template('settings/settings_main.html')

# Нам прислали токен
@socketio.on('sendToken')
def get_token(data) -> None:
    flag: bool

    if token_valid(data):
        flag = True
    else:
        flag = False
    
    socketio.emit("settingsGetToken", flag)

    if flag:
        settings_manager: SettingsManager = SettingsManager()
        asyncio.run(settings_manager.set_setting("bot.token", data))

def token_valid(token: str) -> bool:
    """Проверка того, что токен не инвалид

    Args:
        token (str): Токен

    Returns:
        bool: Правильный ли токен или нет.
    """
    try:
        response = requests.get('https://discord.com/api/v9/users/@me', headers={'Authorization': f'Bot {token}'}) # Немного магии
        response.raise_for_status()

        return True
    
    except Exception:
        return False
