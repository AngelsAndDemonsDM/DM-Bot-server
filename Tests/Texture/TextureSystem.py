import os
import unittest

from PIL import Image

from Code.texture_manager import TextureSystem


class TestTextureSystem(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = 'test_textures.dms'
        os.makedirs(self.test_dir, exist_ok=True)
        
        self.info_yml_content = """
Sprites:
  - name: "sprite1"
    size: {x: 32, y: 32}
    is_mask: false
    frames: 4
  - name: "sprite2"
    size: {x: 32, y: 32}
    is_mask: true
    frames: 4
  - name: "sprite3"
    size: {x: 32, y: 32}
    is_mask: false
    frames: 0
"""
        with open(os.path.join(self.test_dir, 'info.yml'), 'w') as f:
            f.write(self.info_yml_content)
        
        self.sprite1 = Image.new('RGBA', (128, 32), color = (255, 0, 0, 255))
        self.sprite1.save(os.path.join(self.test_dir, 'sprite1.png'))
        
        self.sprite2 = Image.new('RGBA', (128, 32), color = (0, 255, 0, 255))
        self.sprite2.save(os.path.join(self.test_dir, 'sprite2.png'))

        self.sprite3 = Image.new('RGBA', (32, 32), color = (0, 0, 255, 255))
        self.sprite3.save(os.path.join(self.test_dir, 'sprite3.png'))
        
        self.texture_system = TextureSystem(self.test_dir)
        
    def tearDown(self):
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        
        os.rmdir(self.test_dir)
    
    def test_get_texture_and_info(self):
        texture_info = self.texture_system.get_texture_and_info(self.test_dir, 'sprite1')
        self.assertIsNotNone(texture_info)
        image, x, y, is_mask, frame_count = texture_info
        self.assertEqual((x, y), (32, 32))
        self.assertFalse(is_mask)
        self.assertEqual(frame_count, 4)
    
    def test_get_recolor_mask(self):
        color = (0, 0, 255, 255)
        recolored_image = self.texture_system.get_recolor_mask(self.test_dir, 'sprite2', color)
        self.assertIsNotNone(recolored_image)
        self.assertEqual(recolored_image.size, (128, 32))
    
    def test_get_gif(self):
        gif_image = self.texture_system.get_gif(self.test_dir, 'sprite1', fps=5)
        self.assertIsNotNone(gif_image)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'sprite1_compiled.gif')))
    
    def test_get_recolor_gif(self):
        color = (0, 0, 255, 255)
        gif_image = self.texture_system.get_recolor_gif(self.test_dir, 'sprite2', color, fps=5)
        self.assertIsNotNone(gif_image)
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, 'sprite2_compiled_0_0_255_255.gif')))

    def test_merge_layers_static(self):
        layers = [
            {'path': self.test_dir, 'state': 'sprite3', 'color': [255, 0, 0, 255]},
            {'path': self.test_dir, 'state': 'sprite2', 'color': [0, 255, 0, 255]}
        ]
        merged_image = self.texture_system.merge_layers(layers)
        self.assertIsNotNone(merged_image)
        self.assertIsInstance(merged_image, Image.Image)
        self.assertEqual(merged_image.size, (32, 32))

    def test_merge_layers_animated(self):
        layers = [
            {'path': self.test_dir, 'state': 'sprite1', 'color': [255, 0, 0, 255]},
            {'path': self.test_dir, 'state': 'sprite2', 'color': [0, 255, 0, 255]}
        ]
        merged_images = self.texture_system.merge_layers(layers, fps=5)
        self.assertIsNotNone(merged_images)
        self.assertIsInstance(merged_images, list)
        self.assertTrue(all(isinstance(frame, Image.Image) for frame in merged_images))
        self.assertEqual(len(merged_images), 4)

    def test_merge_layers_different_frame_counts(self):
        layers = [
            {'path': self.test_dir, 'state': 'sprite1', 'color': [255, 0, 0, 255]},
            {'path': self.test_dir, 'state': 'sprite3', 'color': [0, 255, 0, 255]}
        ]
        merged_images = self.texture_system.merge_layers(layers, fps=5)
        self.assertIsNotNone(merged_images)
        self.assertIsInstance(merged_images, list)
        self.assertTrue(all(isinstance(frame, Image.Image) for frame in merged_images))
        self.assertEqual(len(merged_images), 4) 
    
    def test_merge_layers_invalid_layer(self):
        layers = [
            {'path': self.test_dir, 'state': 'invalid_sprite', 'color': [255, 0, 0, 255]},
            {'path': self.test_dir, 'state': 'sprite2', 'color': [0, 255, 0, 255]}
        ]
        with self.assertRaises(ValueError):
            self.texture_system.merge_layers(layers, fps=5)

    def test_merge_layers_different_colors(self):
        layers = [
            {'path': self.test_dir, 'state': 'sprite1', 'color': [255, 255, 0, 255]},
            {'path': self.test_dir, 'state': 'sprite2', 'color': [0, 255, 255, 255]}
        ]
        merged_images = self.texture_system.merge_layers(layers, fps=5)
        self.assertIsNotNone(merged_images)
        self.assertIsInstance(merged_images, list)
        self.assertTrue(all(isinstance(frame, Image.Image) for frame in merged_images))
        self.assertEqual(len(merged_images), 4)

if __name__ == '__main__':
    unittest.main()
