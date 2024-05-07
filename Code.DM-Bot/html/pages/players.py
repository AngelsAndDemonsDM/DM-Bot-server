from html.init_socketio import socketio

# TODO: SQL3
from base_classes.file_work import FileWork
from flask import render_template
from player.soul import PlayerSoul

PLAYER_PATH: str = "Discord/players"

def players_main_page():
    return render_template('player.html')

@socketio.on('getAllPlayers')
def handle_get_all_players():
    player_list = []
    try:
        fw = FileWork(PLAYER_PATH)
        players: list[PlayerSoul] = fw.load_data()
        
        for player in players:
            player_dict = {}
            player_dict["id"] = player.id
            player_dict["name"] = player.name
            player_list.append(player_dict)
        
        # Если player_list пустой, добавляем плейсхолдер игрока
    except Exception:
        player_list.append({
            "id": "placeholder",
            "name": "Нет доступных игроков"
        })
        
    socketio.emit('allPlayers', player_list)
