import os

import msgpack
from root_path import ROOT_PATH


class MapManager:
    __slots__ = []

    @staticmethod
    def save_map(map_entity: 'MapEntity', name: str) -> None:  # type: ignore
        """Сохраняет состояние карты в файл.

        Args:
            map_entity (MapEntity): Объект карты, который нужно сохранить.
            name (str): Имя файла, в который будет сохранена карта.
        """
        save_path: str = os.path.join(ROOT_PATH, 'data', 'maps', f'{name}.dmbmap')
        with open(save_path, "wb") as file:
            file.write(msgpack.packb(map_entity, use_bin_type=True))

    @staticmethod
    def load_map(name: str) -> 'MapEntity':  # type: ignore
        """Загружает состояние карты из файла.

        Args:
            name (str): Имя файла, из которого будет загружена карта.

        Returns:
            MapEntity: Объект карты, загруженный из файла.
        """
        load_path: str = os.path.join(ROOT_PATH, 'data', 'maps', f'{name}.dmbmap')
        with open(load_path, "rb") as file:
            map_entity = msgpack.unpackb(file.read(), raw=False)
        
        return map_entity
