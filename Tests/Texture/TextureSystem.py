import hashlib
import os
import pickle
import shutil
import unittest

import yaml
from PIL import Image

from Code.texture_manager import TextureSystem


class TestTextureSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_dir = 'test_sprites'
        os.makedirs(cls.test_dir, exist_ok=True)
        cls.compiled_dir = os.path.abspath(os.path.join(cls.test_dir, 'compiled'))
        os.makedirs(cls.compiled_dir, exist_ok=True)

        info_data = {
            'Sprites': [
                {
                    'name': 'state1',
                    'size': {'x': 100, 'y': 100},
                    'frames': 1,
                    'is_mask': False
                },
                {
                    'name': 'state2',
                    'size': {'x': 150, 'y': 150},
                    'frames': 3,
                    'is_mask': False
                },
                {
                    'name': 'state3',
                    'size': {'x': 200, 'y': 200},
                    'frames': 1,
                    'is_mask': True
                },
                {
                    'name': 'state4',
                    'size': {'x': 250, 'y': 250},
                    'frames': 3,
                    'is_mask': True
                }
            ]
        }
        with open(os.path.join(cls.test_dir, 'info.yml'), 'w') as file:
            yaml.dump(info_data, file)

        for state, (width, height), frames in [
            ('state1', (100, 100), 1), 
            ('state2', (150, 150), 3), 
            ('state3', (200, 200), 1), 
            ('state4', (250, 250), 3)
        ]:
            image = Image.new('RGBA', (width * frames, height), 'white')
            for i in range(frames):
                frame = Image.new('RGBA', (width, height), (i * 85, 255 - i * 85, 0, 255))
                image.paste(frame, (i * width, 0))
            image.save(os.path.join(cls.test_dir, f'{state}.png'))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def test_get_hash_list(self):
        layers = [{'layer1': 'data1'}, {'layer2': 'data2'}]
        expected_hash = hashlib.sha256(pickle.dumps(layers)).hexdigest()
        self.assertEqual(TextureSystem._get_hash_list(layers), expected_hash)

    def test_get_color_str(self):
        color = (255, 128, 64, 32)
        expected_str = '255_128_64_32'
        self.assertEqual(TextureSystem._get_color_str(color), expected_str)

    def test_validate_color(self):
        valid_color = (255, 128, 64, 32)
        try:
            TextureSystem._validate_color(valid_color)
        except ValueError:
            self.fail("_validate_color raised ValueError unexpectedly!")

        invalid_color = (256, 128, 64, 32)
        with self.assertRaises(ValueError):
            TextureSystem._validate_color(invalid_color)

    def test_slice_image(self):
        image = Image.new('RGBA', (450, 150), 'white')
        frames = TextureSystem._slice_image(image, 150, 150, 3)
        self.assertEqual(len(frames), 3)
        for frame in frames:
            self.assertEqual(frame.size, (150, 150))

    def test_get_textures(self):
        textures = TextureSystem.get_textures(self.test_dir)
        expected_textures = [
            {'name': 'state1', 'size': {'x': 100, 'y': 100}, 'frames': 1, 'is_mask': False},
            {'name': 'state2', 'size': {'x': 150, 'y': 150}, 'frames': 3, 'is_mask': False},
            {'name': 'state3', 'size': {'x': 200, 'y': 200}, 'frames': 1, 'is_mask': True},
            {'name': 'state4', 'size': {'x': 250, 'y': 250}, 'frames': 3, 'is_mask': True}
        ]
        self.assertEqual(textures, expected_textures)

    def test_get_state_info(self):
        frame_width, frame_height, num_frames, is_mask = TextureSystem.get_state_info(self.test_dir, 'state1')
        self.assertEqual(frame_width, 100)
        self.assertEqual(frame_height, 100)
        self.assertEqual(num_frames, 1)
        self.assertFalse(is_mask)

        frame_width, frame_height, num_frames, is_mask = TextureSystem.get_state_info(self.test_dir, 'state2')
        self.assertEqual(frame_width, 150)
        self.assertEqual(frame_height, 150)
        self.assertEqual(num_frames, 3)
        self.assertFalse(is_mask)

        frame_width, frame_height, num_frames, is_mask = TextureSystem.get_state_info(self.test_dir, 'state3')
        self.assertEqual(frame_width, 200)
        self.assertEqual(frame_height, 200)
        self.assertEqual(num_frames, 1)
        self.assertTrue(is_mask)

        frame_width, frame_height, num_frames, is_mask = TextureSystem.get_state_info(self.test_dir, 'state4')
        self.assertEqual(frame_width, 250)
        self.assertEqual(frame_height, 250)
        self.assertEqual(num_frames, 3)
        self.assertTrue(is_mask)

    def test_get_compiled(self):
        path = self.test_dir
        state = 'state1'
        color = (255, 255, 255, 255)

        # Test for PNG
        image = TextureSystem.get_image_recolor(path, state, color)
        compiled_image = TextureSystem._get_compiled(path, state, color, is_gif=False)
        self.assertIsNotNone(compiled_image)
        self.assertEqual(compiled_image.size, image.size)

        # Test for GIF
        gif_frames = TextureSystem.get_gif_recolor(path, state, color)
        compiled_gif_frames = TextureSystem._get_compiled(path, state, color, is_gif=True)
        self.assertIsNotNone(compiled_gif_frames)
        self.assertEqual(len(compiled_gif_frames), len(gif_frames))
        for i in range(len(gif_frames)):
            self.assertEqual(compiled_gif_frames[i].size, gif_frames[i].size)

    def test_get_image_recolor(self):
        path = self.test_dir
        state = 'state1'
        color = (255, 0, 0, 255)
        image = TextureSystem.get_image_recolor(path, state, color)
        expected_path = os.path.join(path, f'{state}_compiled_255_0_0_255.png')
        self.assertTrue(os.path.exists(expected_path))
        self.assertEqual(image.size, (100, 100))

    def test_get_image(self):
        path = self.test_dir
        state = 'state1'
        with self.assertRaises(FileNotFoundError):
            TextureSystem.get_image(path, 'non_existing_state')

        image = TextureSystem.get_image(path, state)
        self.assertEqual(image.size, (100, 100))

    def test_get_gif_recolor(self):
        path = self.test_dir
        state = 'state2'
        color = (255, 0, 0, 255)
        gif_frames = TextureSystem.get_gif_recolor(path, state, color)
        expected_path = os.path.join(path, f'{state}_compiled_255_0_0_255.gif')
        self.assertTrue(os.path.exists(expected_path))
        self.assertGreater(len(gif_frames), 0)
        for frame in gif_frames:
            self.assertEqual(frame.size, (150, 150))

    def test_get_gif(self):
        path = self.test_dir
        state = 'state2'
        gif_frames = TextureSystem.get_gif(path, state)
        expected_path = os.path.join(path, f'{state}.gif')
        self.assertTrue(os.path.exists(expected_path))
        self.assertGreater(len(gif_frames), 0)
        for frame in gif_frames:
            self.assertEqual(frame.size, (150, 150))

    def test_merge_layers(self):
        layers = [
            {'path': self.test_dir, 'state': 'state1', 'color': (255, 0, 0, 255)},
            {'path': self.test_dir, 'state': 'state3', 'color': (0, 255, 0, 255)}
        ]
        result_image = TextureSystem.merge_layers(layers)
        self.assertIsNotNone(result_image)
        self.assertEqual(result_image.size, (200, 200))

        layers = [
            {'path': self.test_dir, 'state': 'state2', 'color': (255, 0, 0, 255)},
            {'path': self.test_dir, 'state': 'state4', 'color': (0, 255, 0, 255)}
        ]
        result_gif = TextureSystem.merge_layers(layers)
        self.assertIsNotNone(result_gif)
        self.assertTrue(isinstance(result_gif, list))
        self.assertGreater(len(result_gif), 0)
        for frame in result_gif:
            self.assertEqual(frame.size, (250, 250))


if __name__ == '__main__':
    unittest.main()
