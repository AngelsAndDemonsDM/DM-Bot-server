import os
from typing import List, Optional, Tuple

import yaml
from PIL import Image
from texture_manager.color import RGBColor
from texture_manager.texture_manager import TextureManager
from texture_manager.texture_validator import DMSValidator


class Texture:
    __slots__ = ['_path', '_allow_state']

    def __init__(self, path_to_dms: str) -> None:
        DMSValidator().validate_dms_dirrect(path_to_dms)
        self._path: str = path_to_dms

        self._allow_state: List[Tuple[str, int, bool, Tuple[int, int]]] = []
        self._get_states()

    def _cash_mask(self, mask: str, color: RGBColor) -> None:
        image = TextureManager.recolor_mask(os.path.join(self._path, mask), color)
        save_path = os.path.join(self._path, f"cached_{mask}")
        image.save(save_path, format='PNG')

    def _get_states(self) -> None:
        yml_path = os.path.join(self._path, "info.yml")
        
        with open(yml_path, 'r', encoding='utf-8') as file:
            info_yml = yaml.safe_load(file)
        
        for item in info_yml['Sprites']:
            self._allow_state.append((item['name'], item['is_mask'], item['frames'], (item['size']['x'], item['size']['y'])))

    def get_image(self, state: str) -> Optional[Image.Image]:
        for item in self._allow_state:
            if item[0] == state:
                image_path = os.path.join(self._path, f"{state}.png")
                if os.path.exists(image_path):
                    image = Image.open(image_path)
                    return image
        
        return None

    def __getitem__(self, key: str) -> Optional[Tuple[str, int, bool, Tuple[int, int]]]:
        for item in self._allow_state:
            if item[0] == key:
                return item
        
        return None
