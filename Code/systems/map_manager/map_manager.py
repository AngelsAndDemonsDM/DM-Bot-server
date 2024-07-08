import os
import pickle

from main_impt import ROOT_PATH


class MapManager:
    __slots__ = []

    @staticmethod
    def save_map(map_entity: 'MapEntity', name: str) -> None: # type: ignore
        save_path: str = os.path.join(ROOT_PATH, 'data', 'maps', f'{name}.dmbmap')
        with open(save_path, "wb") as file:
            pickle.dump(map_entity, file)

    @staticmethod
    def load_map(name: str) -> 'MapEntity': # type: ignore
        load_path: str = os.path.join(ROOT_PATH, 'data', 'maps', f'{name}.dmbmap')        
        with open(load_path, "rb") as file:
            map_entity = pickle.load(file)
        
        return map_entity
