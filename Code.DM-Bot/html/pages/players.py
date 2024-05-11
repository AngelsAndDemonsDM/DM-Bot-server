import asyncio
from html.init_socketio import socketio

from flask import render_template
from player import soul_db

PLAYER_PATH: str = "Discord/players"

def players_main_page():
    return render_template('player.html')

@socketio.on('getAllPlayers')
def handle_get_all_players():
    player_list = []

    async def async_task():
        try:
            for user in await soul_db.get_all_records():
                player_list.append({"id": user["id"], "name": user["name"]})

        except Exception:
            player_list.append({
                "id": "placeholder",
                "name": "Нет доступных игроков"
            })

        socketio.emit('allPlayers', player_list)

    asyncio.run(async_task())
