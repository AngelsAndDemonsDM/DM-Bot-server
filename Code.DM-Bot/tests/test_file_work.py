import os
import unittest

from base_classes.file_work import FileWork


class TestFileWork(unittest.TestCase):
    def setUp(self):
        self.file_work = FileWork("test\\test.bin")

    def test_create_file(self):
        self.assertTrue(self.file_work.create_file())
        self.assertTrue(os.path.exists(self.file_work._path))

    def test_load_data(self):
        self.assertIsNone(self.file_work.load_data())
        self.file_work.data = 'test'
        self.assertEqual(self.file_work.load_data(), 'test')

    def test_save_data(self):
        self.file_work.data = 'test'
        self.file_work.save_data()
        self.assertEqual(self.file_work.load_data(), 'test')

    def test_data_property(self):
        self.assertIsNone(self.file_work.data)
        self.file_work.data = 'test'
        self.assertEqual(self.file_work.data, 'test')
