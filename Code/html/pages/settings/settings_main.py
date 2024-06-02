import asyncio
from html.init_socketio import socketio

import requests
from bot import bot_start
from flask import render_template

from Code.main import settings_manager


def render_settings_main_page():
    return render_template('settings/settings_main.html')

# Нам прислали токен
@socketio.on('sendToken')
async def get_token(data) -> None:
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
        await settings_manager.set_setting("token", data)

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

@socketio.on('startBot')
async def start_bot() -> None:
    try:
        asyncio.run(bot_start())
        
    except Exception:
        socketio.emit("anserFromPy", "Токен <p class=\"red\"style=\"display: inline;\">не обнаружен</p>")
