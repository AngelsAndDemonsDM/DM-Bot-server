import asyncio

import requests
from auto_updater import needs_update
from bot.main_bot_core import bot_start
from db_work import SettingsManager
from flask import render_template
from html_code.init_socketio import socketio


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

# Запуск бота
@socketio.on('settingsStartBot')
def handle_start_bot():
    try:
        if asyncio.run(SettingsManager().get_setting("bot.is_run")):
            socketio.emit('settingsBotStartStatus', {'status': 'error', 'message': 'Бот уже запущен!'})
        else:
            socketio.emit('settingsBotStartStatus', {'status': 'success'})
            asyncio.run(bot_start())

    except Exception as e:
        socketio.emit('settingsBotStartStatus', {'status': 'error', 'message': str(e)})

# Работа с автоматическим обновлением
@socketio.on('settingSetUpAutoUpdate')
def get_auto_update(data) -> None:
    flag: bool
    
    try:
        asyncio.run(SettingsManager().set_setting("app.auto_update", data))
        flag = True
    
    except Exception:
        flag = False
    
    socketio.emit("settingAutoUpdateStatusPopup", flag)
    handle_check_auto_update_status()

@socketio.on('settingCheckAutoUpdate')
def handle_check_auto_update_status():
    auto_update = asyncio.run(SettingsManager().get_setting("app.auto_update"))
    socketio.emit('settingAutoUpdateStatusUpdate', auto_update)

# Получение информации о версиях
@socketio.on('getVersionInfo')
def handle_get_version_info():
    _, current_version, latest_version = needs_update()
    
    version_info = {
        "currentVersion": current_version,
        "latestVersion": latest_version
    }
    
    socketio.emit('versionInfo', version_info)
