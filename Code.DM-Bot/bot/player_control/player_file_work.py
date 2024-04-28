import logging

from base_classes import FileWork
from player import PlayerSoul

PLAYER_PATH: str = "Discord/players"

def save_players(data) -> None:
    fw = FileWork(PLAYER_PATH)
    
    fw.data = data
    fw.save_data()

def load_players() -> list[PlayerSoul]:
    fw = FileWork(PLAYER_PATH)

    try:
        data = fw.load_data()
        return data
    except FileNotFoundError:
        return None

def create_dir() -> bool:
    fw = FileWork(PLAYER_PATH)
    return fw.create_file()
