import unittest
from etc.observer import Observer

class TestObserver(unittest.TestCase):
    def setUp(self):
        self.observer = Observer()

    def test_attach(self):
        def func_one():
            pass
        def func_two():
            pass
        self.observer.attach(func_one)
        self.observer.attach(func_two)
        self.assertEqual(self.observer.subscribers, [
            {'func': func_one, 'remaining': -1},
            {'func': func_two, 'remaining': -1}
        ])

    def test_detach(self):
        def func_one():
            pass
        def func_two():
            pass
        self.observer.attach(func_one)
        self.observer.attach(func_two)
        self.observer.detach(func_one)
        self.assertEqual(self.observer.subscribers, [
            {'func': func_two, 'remaining': -1}
        ])

    def test_notify(self):
        def func_one(arg_one, arg_two):
            self.assertEqual(arg_one, 1)
            self.assertEqual(arg_two, 2)
        self.observer.attach(func_one, remaining=1)
        self.observer.notify(1, 2)
        self.assertEqual(self.observer.subscribers, [])
