import unittest

from etc.tag import TagsManager


class TestTagsManager(unittest.TestCase):
    def setUp(self):
        self.tags_manager = TagsManager()

    def test_find(self):
        self.assertFalse(self.tags_manager.find('test'))
        self.tags_manager.add('test')
        self.assertTrue(self.tags_manager.find('test'))

    def test_add(self):
        self.assertTrue(self.tags_manager.add('test'))
        self.assertFalse(self.tags_manager.add('test'))

    def test_remove(self):
        self.assertFalse(self.tags_manager.remove('test'))
        self.tags_manager.add('test')
        self.assertTrue(self.tags_manager.remove('test'))

    def test_sort(self):
        self.tags_manager.add('c')
        self.tags_manager.add('b')
        self.tags_manager.add('a')
        self.tags_manager.sort()
        self.assertEqual(self.tags_manager._ids, ['a', 'b', 'c'])
