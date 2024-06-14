import argparse
import asyncio
import logging
import signal
import sys
import webbrowser
from html.init_socketio import handle_show_popup, socketio
from html.main_routes import main_bp

from bot import bot_close, bot_start
from colorlog import ColoredFormatter
from db_work import SettingsManager
from flask import Flask

VERSION: str = "0.0.04"

app = Flask(__name__)

socketio.init_app(app)

# Blueprint
app.register_blueprint(main_bp)

# Argument parsing
def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    parser.add_argument('--version', action='store_true', help='Возвращает версию приложения')
    return parser.parse_args()

# Async helper function
async def async_main_bg_task():
    if await SettingsManager().get_setting("bot.auto_start"):
        await SettingsManager().set_setting("bot.is_run", False) # Хуйня ебаная. async_main_bg_task должна быть вызвана только при запуске, так что оправдано.
        await bot_start()

async def shutdown_app():
    logging.info("Shutdown bot...")
    await bot_close()
    logging.info("Done!")
    
# Background task function
def main_bg_task():
    asyncio.run(async_main_bg_task())

# Signals
def handle_exit_signal(signum, frame):
    logging.info("Shutdown start")
    asyncio.run(shutdown_app())
    
    logging.info("Shutdown app is done!")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit_signal)

# Start program
if __name__ == "__main__":
    args = parse_arguments()
    version = args.version
    debug = args.debug
    
    if version:
        print(VERSION)
        sys.exit(0)
    
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)        
    else:
        logger.setLevel(logging.INFO)
    logger.handlers.clear()
    
    console_handler = logging.StreamHandler()
    formatter = ColoredFormatter(
        "[%(asctime)s] [%(log_color)s%(levelname)s%(reset)s] - %(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'purple',
        },
        secondary_log_colors={},
        style='%'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    if not debug:
        webbrowser.open("http://127.0.0.1:5000")
    
    socketio.start_background_task(main_bg_task)
    
    socketio.run(app, debug=debug, allow_unsafe_werkzeug=True)
