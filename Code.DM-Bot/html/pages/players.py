from flask import render_template
from html.init_socketio import socketio

def players_main_page():
    return render_template('player.html')


@socketio.on('getAllPlayers')
def handle_get_all_players():
    socketio.emit('allPlayers', [{'id': 456381306553499649, 'name': 'cainheretic'}, {'id': 295851102010605569, 'name': 'vergrey'}])
