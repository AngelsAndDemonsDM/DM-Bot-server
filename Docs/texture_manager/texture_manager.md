# Документация по файлу `texture_manager.py`


## `TextureManager.recolor_mask`<br>
Перекрашивает маску изображения в заданный цвет.<br>
**Args:**<br>
mask_image (Image.Image): Изображение маски, которое нужно перекрасить.<br>
color (Union[HEXColor, RGBColor]): Цвет, в который будет перекрашена маска. Может быть представлен как HEXColor или RGBColor.<br>
**Raises:**<br>
ValueError: Если цвет не является экземпляром HEXColor или RGBColor.<br>
**Returns:**<br>
Image.Image: Перекрашенное изображение маски.<br>
<br>
