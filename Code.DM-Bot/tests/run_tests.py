import os
import shutil
import unittest

from .test_file_work import TestFileWork
from .test_observer import TestObserver
from .test_tag import TestTagsManager


def del_test_folder() -> None: 
    test_folder_path = os.path.join(os.getcwd(), 'Data.DM-Bot', 'test')
    if os.path.exists(test_folder_path):
        shutil.rmtree(test_folder_path)

def run_tests() -> None:
    """
    Запускает тесты из папки tests.

    Перед и после запуска тестов проверяет, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.
    """
    del_test_folder()

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestObserver))
    suite.addTests(loader.loadTestsFromTestCase(TestFileWork))
    suite.addTests(loader.loadTestsFromTestCase(TestTagsManager))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    del_test_folder()
    
    return
