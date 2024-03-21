import asyncio
import os
import shutil

from tests.test_file_work import test_FileWork
from tests.test_organ import test_Organ, test_OrganPrototype
from tests.test_tag_system import test_Tag, test_TagsManager


def del_test_folder(logger): 
    test_folder_path = os.path.join(os.getcwd(), 'Data.DM-Bot', 'test')
    if os.path.exists(test_folder_path):
        shutil.rmtree(test_folder_path)
        logger.debug("Test folder deleted successfully.")    

async def run_tests(logger):
    """
    Запускает тесты из папки tests.

    Перед и после запуска тестов проверяет, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.

    Returns:
        bool: True, если все тесты успешно пройдены, в противном случае False.
    """
    del_test_folder(logger)
    
    all_tests_passed = True
    
    logger.debug("===START TESTS===")
    
    logger.debug("="*40)
    logger.debug("Start test_FileWork")
    all_tests_passed &= await test_FileWork(logger)
    
    logger.debug("="*40)
    logger.debug("Start test_TagData")
    all_tests_passed &= await test_Tag(logger)
    
    logger.debug("="*40)
    logger.debug("Start test_TagsManager")
    all_tests_passed &= await test_TagsManager(logger)
    
    logger.debug("="*40)
    logger.debug("Start test_Organ")
    all_tests_passed &= await test_Organ(logger)

    logger.debug("="*40)
    logger.debug("Start test_OrganPrototype")
    all_tests_passed &= await test_OrganPrototype(logger)

    logger.debug("="*40)
    del_test_folder(logger)
    
    logger.debug("===END TESTS===")
    
    return all_tests_passed
