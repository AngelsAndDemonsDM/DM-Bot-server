from flask import render_template
from html.init_socketio import socketio
from base_classes.file_work import FileWork
from player.soul import PlayerSoul

def players_main_page():
    return render_template('player.html')


@socketio.on('getAllPlayers')
def handle_get_all_players():
    player_list = []
    players:list [PlayerSoul] = FileWork("Discord/players")
    
    for player in players:
        player_dict = {}

        player_dict["id"] = player.id
        player_dict["name"] = player.name

        player_list.append(player_dict)
    
    socketio.emit('allPlayers', player_list)
