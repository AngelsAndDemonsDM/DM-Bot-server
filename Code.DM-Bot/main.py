import argparse
import logging
import sys
import webbrowser

from colorlog import ColoredFormatter
from flask import Flask
from flask_socketio import SocketIO
from main_vars import VERSION
from pages.about import about
from pages.index import index

app = Flask(__name__)
socketio = SocketIO(app)

def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    parser.add_argument('--version', action='store_true', help='Возвращает версию приложения')
    return parser.parse_args()

# Pages
@app.route('/')
def home_page():
    return index()

@app.route('/about')
def about_page():
    return about()

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
    
    socketio.run(app, debug=debug, allow_unsafe_werkzeug=True)
