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
        return fw.load_data()
    except FileNotFoundError:
        return False

def create_dir() -> bool:
    fw = FileWork(PLAYER_PATH)
    return fw.create_file()
