import asyncio
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template
from flask_socketio import SocketIO
from bot import BOT_STATUS, bot_shutdown, bot_start, bot_status

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bot')
def bot():
    return render_template('bot.html', bot_status=BOT_STATUS)

def run_async_function_in_thread(async_func):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_func())

@socketio.on('start_bot')
def soket_bot_start():
    with ThreadPoolExecutor() as executor:
        executor.submit(run_async_function_in_thread, bot_start)

@socketio.on('shutdown_bot')
def soket_bot_shutdown():
    with ThreadPoolExecutor() as executor:
        executor.submit(run_async_function_in_thread, bot_shutdown)

@socketio.on('status_bot')
def soket_bot_status():
    status = bot_status()
    socketio.emit('update_bot_status', status)

if __name__ == '__main__':
    socketio.run(app, debug=True)
