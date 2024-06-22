from typing import Union

from PIL import Image

from Code.texture_manager import HEXColor, RGBColor


class TextureManager:
    __slots__ = []
    
    def __init__(self) -> None:
        pass

    @staticmethod
    def recolor_mask(mask_path: str, color: Union[HEXColor, RGBColor]) -> Image.Image:
        if isinstance(color, HEXColor):
            color = color.get_rgba()
        
        elif isinstance(color, RGBColor):
            color = color.cur_value
        
        else:
            raise ValueError("The color passed to recolor_mask must be an instance of HEXColor or RGBColor")

        mask_image = Image.open(mask_path).convert("RGBA")
       
        new_data = [
            (
                int(pixel[0] * color[0] / 255),
                int(pixel[0] * color[1] / 255),
                int(pixel[0] * color[2] / 255),
                pixel[3]
            ) if pixel[3] != 0 else pixel
            for pixel in mask_image.getdata()
        ]
        mask_image.putdata(new_data)
        
        return mask_image
