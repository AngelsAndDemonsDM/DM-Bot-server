import unittest

from Code.texture_manager import HEXColor


class TestHEXColor(unittest.TestCase):
    def test_initialization_valid(self):
        color = HEXColor("#FFAABB")
        self.assertEqual(color.cur_value, "#FFAABB")
        color_with_alpha = HEXColor("FFAABBCC")
        self.assertEqual(color_with_alpha.cur_value, "#FFAABBCC")

    def test_initialization_invalid(self):
        with self.assertRaises(ValueError):
            HEXColor("ZZZZZZ")
        with self.assertRaises(ValueError):
            HEXColor("12345")
        with self.assertRaises(ValueError):
            HEXColor("#12345Z")

    def test_setter_valid(self):
        color = HEXColor("000000")
        color.cur_value = "#123456"
        self.assertEqual(color.cur_value, "#123456")
        color.cur_value = "AABBCCDD"
        self.assertEqual(color.cur_value, "#AABBCCDD")

    def test_setter_invalid(self):
        color = HEXColor("000000")
        with self.assertRaises(ValueError):
            color.cur_value = "GGGGGG"
        with self.assertRaises(ValueError):
            color.cur_value = "#12345"
        with self.assertRaises(ValueError):
            color.cur_value = "ZZZZZZ"

    def test_get_rgba(self):
        color = HEXColor("FFAABB")
        self.assertEqual(color.get_rgba(), (255, 170, 187, 255))
        color_with_alpha = HEXColor("FFAABBCC")
        self.assertEqual(color_with_alpha.get_rgba(), (255, 170, 187, 204))

if __name__ == '__main__':
    unittest.main()
