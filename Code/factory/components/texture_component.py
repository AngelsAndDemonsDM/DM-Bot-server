from typing import Any, Dict, List

from factory.base_component import Component


class TextureComponent(Component):
    __slots__ = ['layers']

    def __init__(self, layers=None):
        super().__init__()
        self.layers = layers if layers is not None else self.default_values()['layers']

    def __repr__(self):
        return f"TextureComponent(layers={self.layers})"

    @classmethod
    def default_values(cls) -> Dict[str, Dict[str, Any]]:
        return {'layers': {'not_found': {'path': 'dev/error', 'color': [255, 255, 255, 255]}}}

    def get_layers(self) -> List[Dict[str, Any]]:
        """Возвращает все слои в виде списка словарей.

        Returns:
            List[Dict[str, Any]]: Список слоев, каждый из которых является словарем с ключами 'state', 'path' и 'color'.
        """
        return [{'state': state, 'path': info['path'], 'color': info['color']} for state, info in self.layers.items()]
    
    def add_layer(self, state: str, path: str, color: List[int] = [255, 255, 255, 255]) -> None:
        """Добавляет слой в компонент.

        Args:
            state (str): Состояние слоя.
            path (str): Путь к текстуре слоя.
            color (List[int], optional): Цвет слоя в формате RGBA. По умолчанию [255, 255, 255, 255].
        """
        self.layers[state] = {'path': path, 'color': color}

    def remove_layer(self, state: str) -> None:
        """Удаляет слой из компонента по его состоянию.

        Args:
            state (str): Состояние слоя, которое нужно удалить.
        """
        if state in self.layers:
            del self.layers[state]

    def get_layer_path(self, state: str) -> str:
        """Возвращает путь к текстуре слоя по его состоянию.

        Args:
            state (str): Состояние слоя.

        Returns:
            str: Путь к текстуре слоя или None, если слой не найден.
        """
        layer = self.layers.get(state)
        return layer['path'] if layer else None

    def get_layer_color(self, state: str) -> List[int]:
        """Возвращает цвет слоя по его состоянию.

        Args:
            state (str): Состояние слоя.

        Returns:
            List[int]: Цвет слоя в формате RGBA или None, если слой не найден.
        """
        layer = self.layers.get(state)
        return layer['color'] if layer else None
