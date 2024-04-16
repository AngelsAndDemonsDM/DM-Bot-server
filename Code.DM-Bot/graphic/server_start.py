import argparse
import logging

from colorlog import ColoredFormatter
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

game_state = {
    'score': 0,
    'message': 'Добро пожаловать в игру!'
}

@app.route('/')
def home():
    return render_template('index.html', game_state=game_state)

@socketio.on('increment_score')
def handle_increment_score():
    game_state["score"] += 1
    socketio.emit('update_score', game_state["score"])

def parse_arguments():
    parser = argparse.ArgumentParser(description='DM-Bot')
    parser.add_argument('--debug', action='store_true', help='Включить режим отладки')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    debug = args.debug

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

    socketio.run(app, debug=debug)
