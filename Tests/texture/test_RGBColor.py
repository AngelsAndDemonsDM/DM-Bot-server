import unittest

from Code.texture_manager import RGBColor


class TestRGBColor(unittest.TestCase):
    def test_initialization_valid(self):
        color = RGBColor((255, 100, 50, 255))
        self.assertEqual(color.cur_value, (255, 100, 50, 255))

    def test_initialization_invalid(self):
        with self.assertRaises(ValueError):
            RGBColor((256, 100, 50, 255))
        with self.assertRaises(ValueError):
            RGBColor((255, 100, 50, -1))

    def test_setter_valid(self):
        color = RGBColor((0, 0, 0, 0))
        color.cur_value = (128, 128, 128, 128)
        self.assertEqual(color.cur_value, (128, 128, 128, 128))

    def test_setter_invalid(self):
        color = RGBColor((0, 0, 0, 0))
        with self.assertRaises(ValueError):
            color.cur_value = (300, 0, 0, 0)
        with self.assertRaises(ValueError):
            color.cur_value = (0, 0, 0, 256)

    def test_get_hex(self):
        color = RGBColor((255, 0, 0, 255))
        self.assertEqual(color.get_hex(), '#FF0000')
        color_with_alpha = RGBColor((255, 0, 0, 128))
        self.assertEqual(color_with_alpha.get_hex(), '#FF000080')

if __name__ == '__main__':
    unittest.main()
