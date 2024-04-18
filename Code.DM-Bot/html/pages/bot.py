from flask import render_template
from html.init_socketio import socketio


def bot_main_page():
    return render_template('bot.html')

# Нам прислали токен, пируем
@socketio.on('sendToken')
def get_token(data):
    socketio.emit("anserFromPy", f"Иди нахуй {data}")

# Отправка статуса бота
@socketio.on('requestBotStatus')
def send_bot_status():
    socketio.emit("getBotStatus", True)
