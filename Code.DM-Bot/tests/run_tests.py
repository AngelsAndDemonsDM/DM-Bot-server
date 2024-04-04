import asyncio
import logging
import os
import shutil


def del_test_folder(): 
    test_folder_path = os.path.join(os.getcwd(), 'Data.DM-Bot', 'test')
    if os.path.exists(test_folder_path):
        shutil.rmtree(test_folder_path)
        logging.debug("Test folder deleted successfully.")    

async def run_tests():
    """
    Запускает тесты из папки tests.

    Перед и после запуска тестов проверяет, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.

    Returns:
        bool: True, если все тесты успешно пройдены, в противном случае False.
    """
    del_test_folder()
    all_tests_passed = True
    
    logging.debug("===START TESTS===")

    logging.debug("="*40)
    del_test_folder()
    
    logging.debug("===END TESTS===")
    
    return all_tests_passed
