import asyncio
from html.init_socketio import socketio

from flask import render_template
from player import soul_db

PLAYER_PATH: str = "Discord/players"

def render_players_main_page():
    return render_template('player.html')

@socketio.on('getAllPlayers')
def handle_get_all_players():
    player_list = []

    async def async_task():
        async with soul_db:
            try:
                users = await soul_db.select("souls")
                if users:
                    for user in users:
                        player_list.append({"id": user["discord_id"], "name": user["name"]})
                else:
                    player_list.append({
                        "id": "???",
                        "name": "Нет доступных игроков"
                    })
    
            except Exception:
                player_list.append({
                    "id": "???",
                    "name": "Ошибка при получении игроков"
                })
    
        socketio.emit('allPlayers', player_list)
        await soul_db.close()

    asyncio.run(async_task())
