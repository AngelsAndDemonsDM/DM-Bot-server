import os
import unittest

from PIL import Image

from Code.texture_manager import TextureSystem


class TestTextureSystem(unittest.TestCase):

    def setUp(self):
        self.test_dir = 'test_sprites'
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.info_content = """
        Sprites:
          - name: state1
            is_mask: true
            size:
              x: 32
              y: 32
            frames: 1
          - name: state2
            is_mask: false
            size:
              x: 64
              y: 64
            frames: 2
        """
        
        with open(f"{self.test_dir}/info.yml", "w") as f:
            f.write(self.info_content)

        image = Image.new("RGBA", (32, 32), (255, 0, 0, 255))
        image.save(f"{self.test_dir}/state1.png")
        
        image = Image.new("RGBA", (128, 64), (0, 255, 0, 255))
        image.save(f"{self.test_dir}/state2.png")
    
    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def test_init(self):
        ts = TextureSystem(self.test_dir)
        self.assertTrue(os.path.exists(ts._sprite_path))

    def test_get_color_str(self):
        color = (255, 128, 64, 32)
        self.assertEqual(TextureSystem._get_color_str(color), '255_128_64_32')

    def test_validate_color_valid(self):
        color = (255, 128, 64, 32)
        try:
            TextureSystem._validate_color(color)
        except ValueError:
            self.fail("Unexpected ValueError raised")

    def test_validate_color_invalid(self):
        color = (256, 128, 64, 32)
        with self.assertRaises(ValueError):
            TextureSystem._validate_color(color)

    def test_get_texture_states(self):
        path = self.test_dir
        result = TextureSystem._get_texture_states(path)
        expected = [
            {'name': 'state1', 'is_mask': True, 'size': {'x': 32, 'y': 32}, 'frames': 1},
            {'name': 'state2', 'is_mask': False, 'size': {'x': 64, 'y': 64}, 'frames': 2}
        ]
        self.assertEqual(result, expected)
    
    def test_is_mask(self):
        path = self.test_dir
        state = 'state1'
        self.assertTrue(TextureSystem.is_mask(path, state))
        state = 'state2'
        self.assertFalse(TextureSystem.is_mask(path, state))
    
    def test_get_texture_and_info(self):
        ts = TextureSystem(self.test_dir)
        result = ts.get_texture_and_info(self.test_dir, 'state1')
        
        self.assertIsNotNone(result)
        self.assertEqual(result[1], 32)
        self.assertEqual(result[2], 32)
        self.assertTrue(result[3])
        self.assertEqual(result[4], 1)

    def test_get_recolor_mask_valid(self):
        ts = TextureSystem(self.test_dir)
        path = self.test_dir
        state = 'state1'
        color = (255, 128, 64, 32)

        result = ts.get_recolor_mask(path, state, color)
        self.assertIsInstance(result, Image.Image)

    def test_get_recolor_mask_invalid(self):
        ts = TextureSystem(self.test_dir)
        path = self.test_dir
        state = 'state2'
        color = (255, 128, 64, 32)

        with self.assertRaises(ValueError):
            ts.get_recolor_mask(path, state, color)
    
    def test_get_gif(self):
        ts = TextureSystem(self.test_dir)
        path = self.test_dir
        state = 'state2'
        
        gif = ts.get_gif(path, state, fps=24)
        self.assertIsInstance(gif, list)

    def test_get_recolor_gif(self):
        ts = TextureSystem(self.test_dir)
        path = self.test_dir
        state = 'state1'
        color = (255, 128, 64, 32)
        
        gif = ts.get_recolor_gif(path, state, color, fps=24)
        self.assertIsInstance(gif, list)
    
    def test_get_compiled_texture_mask(self):
        ts = TextureSystem(self.test_dir)
        path = self.test_dir
        state = 'state1'
        color = (255, 128, 64, 32)
        
        compiled_texture = ts.get_compiled_texture(path, state, color, fps=24)
        self.assertIsInstance(compiled_texture, Image.Image)

    def test_get_compiled_texture_animation(self):
        ts = TextureSystem(self.test_dir)
        path = self.test_dir
        state = 'state2'
        
        compiled_texture = ts.get_compiled_texture(path, state, fps=24)
        self.assertIsInstance(compiled_texture, list)

    def test_slice_image(self):
        image = Image.new("RGBA", (128, 64), (0, 255, 0, 255))
        frames = TextureSystem._slice_image(image, 64, 32, 2)
        self.assertEqual(len(frames), 2)
        self.assertIsInstance(frames[0], Image.Image)
        self.assertIsInstance(frames[1], Image.Image)

    def test_create_gif(self):
        frames = [Image.new("RGBA", (64, 32), (i*50, i*50, i*50, 255)) for i in range(5)]
        gif_path = os.path.join(self.test_dir, "test.gif")
        
        TextureSystem._create_gif(frames, gif_path, duration=100)
        self.assertTrue(os.path.exists(gif_path))
        
        with Image.open(gif_path) as gif:
            self.assertTrue(gif.is_animated)
            self.assertEqual(gif.n_frames, 5)

if __name__ == '__main__':
    unittest.main()
