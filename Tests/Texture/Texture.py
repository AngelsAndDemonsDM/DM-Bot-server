import unittest
from unittest.mock import mock_open, patch

from PIL import Image

from Code.texture_manager import RGBColor, Texture


class TestTexture(unittest.TestCase):
    @patch('builtins.open', new_callable=mock_open, read_data='Sprites: []')
    @patch('os.path.exists', return_value=True)
    @patch('texture_manager.texture_validator.DMSValidator.validate_dms_dirrect')
    def test_initialization(self, mock_validate, mock_exists, mock_open):
        texture = Texture('/fake/path')
        self.assertEqual(texture._path, '/fake/path')
        self.assertEqual(texture._allow_state, [])
        mock_validate.assert_called_once_with('/fake/path')

    @patch('os.path.exists', return_value=True)
    @patch('yaml.safe_load', return_value={'Sprites': [{'name': 'state1', 'is_mask': 1, 'frames': 10, 'size': {'x': 64, 'y': 64}}]})
    @patch('builtins.open', new_callable=mock_open)
    def test_load_states(self, mock_open, mock_yaml, mock_exists):
        texture = Texture('/fake/path')
        texture._load_states()
        self.assertEqual(len(texture._allow_state), 1)
        self.assertEqual(texture._allow_state[0], ('state1', 1, 10, (64, 64)))

    @patch('os.path.exists', return_value=True)
    @patch('PIL.Image.open', return_value=Image.new('RGBA', (64, 64)))
    def test_get_image(self, mock_open, mock_exists):
        texture = Texture('/fake/path')
        image = texture.get_image('state1')
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (64, 64))

    @patch('os.path.exists', return_value=True)
    @patch('PIL.Image.open', return_value=Image.new('RGBA', (128, 128)))
    @patch('PIL.Image.Image.crop', return_value=Image.new('RGBA', (64, 64)))
    @patch('texture_manager.texture_manager.TextureManager.recolor_mask', return_value=Image.new('RGBA', (64, 64)))
    def test_create_gif(self, mock_recolor, mock_crop, mock_open, mock_exists):
        texture = Texture('/fake/path')
        texture._allow_state = [('state1', 1, 10, (64, 64))]
        with patch.object(Image.Image, 'save', return_value=None) as mock_save:
            texture.create_gif('state1')
            self.assertEqual(mock_save.call_count, 1)

    @patch('os.path.exists', return_value=False)
    @patch('texture.Texture._cache_mask_image')
    @patch('PIL.Image.open', return_value=Image.new('RGBA', (64, 64)))
    def test_get_cached_mask(self, mock_open, mock_cache, mock_exists):
        texture = Texture('/fake/path')
        color = RGBColor(255, 0, 0)
        image = texture.get_cached_mask('state1', color)
        mock_cache.assert_called_once_with('state1', color)
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (64, 64))

    @patch('os.path.exists', return_value=False)
    @patch('texture.Texture.create_gif')
    @patch('PIL.Image.open', return_value=Image.new('RGBA', (64, 64)))
    def test_get_cached_gif(self, mock_open, mock_create_gif, mock_exists):
        texture = Texture('/fake/path')
        image = texture.get_cached_gif('state1')
        mock_create_gif.assert_called_once_with('state1', 60)
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (64, 64))

    @patch('os.path.exists', return_value=False)
    @patch('PIL.Image.open', return_value=Image.new('RGBA', (128, 128)))
    @patch('PIL.Image.Image.crop', return_value=Image.new('RGBA', (64, 64)))
    @patch('texture_manager.texture_manager.TextureManager.recolor_mask', return_value=Image.new('RGBA', (64, 64)))
    def test_create_colored_gif(self, mock_recolor, mock_crop, mock_open, mock_exists):
        texture = Texture('/fake/path')
        texture._allow_state = [('state1', 1, 10, (64, 64))]
        color = RGBColor(255, 0, 0)
        with patch.object(Image.Image, 'save', return_value=None) as mock_save:
            texture.create_colored_gif('state1', color)
            self.assertEqual(mock_save.call_count, 1)


if __name__ == '__main__':
    unittest.main()
