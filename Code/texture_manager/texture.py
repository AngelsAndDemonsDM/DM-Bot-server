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
        DMSValidator.validate_dms_dirrect(path_to_dms)
        self._path: str = path_to_dms
        self._allow_state: List[Tuple[str, bool, int, Tuple[int, int]]] = []
        self._load_states()

    def _load_states(self) -> None:
        yml_path = os.path.join(self._path, "info.yml")
        with open(yml_path, 'r', encoding='utf-8') as file:
            info_yml = yaml.safe_load(file)

        self._allow_state = [
            (item['name'], item['is_mask'], item['frames'], (item['size']['x'], item['size']['y']))
            for item in info_yml['Sprites']
        ]

    def _cache_mask_image(self, mask: str, color: RGBColor) -> None:
        mask_image = Image.open(os.path.join(self._path, f"{mask}.png")).convert("RGBA")
        image = TextureManager.recolor_mask(mask_image, color)
        save_path = os.path.join(self._path, f"cached_{mask}_{color.get_hex()}.png")
        image.save(save_path, format='PNG')

    def _generate_gif_frames(self, sprite_image: Image.Image, state_info: Tuple[str, bool, int, Tuple[int, int]], fps: int, color: Optional[RGBColor] = None) -> Tuple[List[Image.Image], int]:
        name, is_mask, frames, (frame_width, frame_height) = state_info
        sprite_width, sprite_height = sprite_image.size
        gif_frames = []
        frame_duration = int(1000 / fps)

        for y in range(0, sprite_height, frame_height):
            for x in range(0, sprite_width, frame_width):
                if len(gif_frames) >= frames:
                    return gif_frames, frame_duration
                box = (x, y, x + frame_width, y + frame_height)
                frame = sprite_image.crop(box)
                if color and is_mask:
                    frame = TextureManager.recolor_mask(frame, color)
                gif_frames.append(frame)

        return gif_frames, frame_duration

    def __getitem__(self, key: str) -> Optional[Tuple[str, bool, int, Tuple[int, int]]]:
        return next((item for item in self._allow_state if item[0] == key), None)

    def get_image(self, state: str) -> Optional[Image.Image]:
        image_path = os.path.join(self._path, f"{state}.png")
        return Image.open(image_path) if os.path.exists(image_path) else None

    def create_gif(self, state: str, fps: int = 60) -> None:
        state_info = self[state]
        if state_info is None:
            raise ValueError(f"State '{state}' not found in Texture.")

        sprite_image = self.get_image(state)
        if sprite_image is None:
            raise FileNotFoundError(f"Image for state '{state}' not found.")

        gif_frames, frame_duration = self._generate_gif_frames(sprite_image, state_info, fps)
        output_path = os.path.join(self._path, f"{state}.gif")
        gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:], optimize=False, duration=frame_duration, loop=0)

    def get_cached_mask(self, state: str, color: RGBColor) -> Image.Image:
        cache_file = os.path.join(self._path, f"cached_{state}_{color.get_hex()}.png")
        if not os.path.exists(cache_file):
            self._cache_mask_image(state, color)
        return Image.open(cache_file)

    def get_cached_gif(self, state: str, fps: int = 60) -> Image.Image:
        gif_file = os.path.join(self._path, f"{state}.gif")
        if not os.path.exists(gif_file):
            self.create_gif(state, fps)
        return Image.open(gif_file)

    def create_colored_gif(self, state: str, color: RGBColor, fps: int = 60) -> Image.Image:
        state_info = self[state]
        if state_info is None:
            raise ValueError(f"State '{state}' not found in Texture.")

        sprite_image = self.get_image(state)
        if sprite_image is None:
            raise FileNotFoundError(f"Image for state '{state}' not found.")

        gif_frames, frame_duration = self._generate_gif_frames(sprite_image, state_info, fps, color)
        output_path = os.path.join(self._path, f"cached_{state}_{color.get_hex()}.gif")
        gif_frames[0].save(output_path, save_all=True, append_images=gif_frames[1:], optimize=False, duration=frame_duration, loop=0)

        return Image.open(output_path)
