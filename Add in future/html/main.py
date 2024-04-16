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

if __name__ == '__main__':
    socketio.run(app, debug=True)
