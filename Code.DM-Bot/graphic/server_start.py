import asyncio

from bot import BotWeb
from flask import Flask, redirect, render_template, request, url_for
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

BOT: BotWeb = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bot', methods=['GET', 'POST'])
def bot():
    global BOT

    if request.method == 'POST':
        token = request.form.get('token')
        if token:
            BOT = BotWeb(token)

    if BOT is not None:
        status = BOT.status_str_html()
    else:
        status = "N/D"

    return render_template('bot.html', bot_status=status, bot_create= False if BOT is None else True)

@socketio.on('start_bot')
def soket_bot_start():
    global BOT

    if BOT is None:
        return

    asyncio.run(BOT.start())    

@socketio.on('status_bot')
def soket_bot_status():
    global BOT

    if BOT is None:
        res = "N/D"
    else:
        res = BOT.status_str_html()

    socketio.emit('update_bot_status', res)

if __name__ == '__main__':
    socketio.run(app, debug=True)
