import os
import shutil
import tempfile
import unittest

import yaml
from PIL import Image

from Code.texture_manager import DMSValidator, RGBColor, Texture


class TestTexture(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

        self.info_yml_path = os.path.join(self.test_dir, "info.yml")
        with open(self.info_yml_path, 'w') as file:
            yaml.dump({'Sprites': [{'name': 'state1', 'is_mask': 1, 'frames': 10, 'size': {'x': 64, 'y': 64}}]}, file)

        self.image_path = os.path.join(self.test_dir, "state1.png")
        image = Image.new('RGBA', (128, 128))
        image.save(self.image_path)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_initialization(self):
        texture = Texture(self.test_dir)
        self.assertEqual(texture._path, self.test_dir)
        self.assertEqual(texture._allow_state, [])
        DMSValidator.validate_dms_dirrect(self.test_dir)

    def test_load_states(self):
        texture = Texture(self.test_dir)
        texture._load_states()
        self.assertEqual(len(texture._allow_state), 1)
        self.assertEqual(texture._allow_state[0], ('state1', 1, 10, (64, 64)))

    def test_get_image(self):
        texture = Texture(self.test_dir)
        image = texture.get_image('state1')
        self.assertIsNotNone(image)
        self.assertEqual(image.size, (128, 128))

    def test_create_gif(self):
        texture = Texture(self.test_dir)
        texture._allow_state = [('state1', 1, 10, (64, 64))]
        texture.create_gif('state1')
        gif_path = os.path.join(self.test_dir, 'state1.gif')
        self.assertTrue(os.path.exists(gif_path))

    def test_get_cached_mask(self):
        texture = Texture(self.test_dir)
        color = RGBColor((255, 0, 0, 255))
        cached_mask = texture.get_cached_mask('state1', color)
        cached_mask_path = os.path.join(self.test_dir, f'cached_state1_{color.get_hex()}.png')
        self.assertTrue(os.path.exists(cached_mask_path))
        self.assertIsNotNone(cached_mask)
        self.assertEqual(cached_mask.size, (64, 64))

    def test_get_cached_gif(self):
        texture = Texture(self.test_dir)
        cached_gif = texture.get_cached_gif('state1')
        cached_gif_path = os.path.join(self.test_dir, 'state1.gif')
        self.assertTrue(os.path.exists(cached_gif_path))
        self.assertIsNotNone(cached_gif)
        self.assertEqual(cached_gif.size, (128, 128))

    def test_create_colored_gif(self):
        texture = Texture(self.test_dir)
        texture._allow_state = [('state1', 1, 10, (64, 64))]
        color = RGBColor((255, 0, 0, 255))
        colored_gif = texture.create_colored_gif('state1', color)
        colored_gif_path = os.path.join(self.test_dir, f'cached_state1_{color.get_hex()}.gif')
        self.assertTrue(os.path.exists(colored_gif_path))
        self.assertIsNotNone(colored_gif)
        self.assertEqual(colored_gif.size, (128, 128))


if __name__ == '__main__':
    unittest.main()
