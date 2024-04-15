import asyncio
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template
from flask_socketio import SocketIO
from bot import bot_start, bot_status

app = Flask(__name__)
socketio = SocketIO(app)

BOT_STATUS = "N/D"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bot')
def bot():
    return render_template('bot.html', bot_status=BOT_STATUS)

def run_bot_thread(async_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_func())

@socketio.on('start_bot')
def soket_bot_start():
    with ThreadPoolExecutor() as executor:
        executor.submit(run_bot_thread, bot_start)

@socketio.on('status_bot')
def soket_bot_status():
    global BOT_STATUS

    BOT_STATUS = bot_status()
    socketio.emit('update_bot_status', BOT_STATUS)

if __name__ == '__main__':
    socketio.run(app, debug=True)
