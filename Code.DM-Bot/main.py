import asyncio
import os
import shutil

from etc.logger import LoggerManager
from tests.test_file_work import test_FileWork
from tests.test_tag_system import test_Tag, test_TagsManager


def del_test_folder(logger):
    test_folder_path = os.path.join(os.getcwd(), 'data', 'test')
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
    del_test_folder(logger)
    
    logger.debug("===END TESTS===")
    
    return all_tests_passed

def show_menu():
    while True:
        print("\nМеню выбора:")
        print("1. Запуск тестов")
        print("0. Выход")
        choice = input("Введите число: ")
        if choice in {"0", "1"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")

async def main():
    # Инициализация дебага
    while True:
        debug = input("Debug? (Y/N): ").strip().upper()
        if debug in {"Y", "N"}:
            debug = debug == "Y"
            break
        else:
            print("Error. It must be 'Y' or 'N'!")

    # Объявление менеджеров
    logger = LoggerManager(debug)

    # Меню выбора
    while True:
        menu = show_menu()
        
        if menu == 1: # Запуск тестов
            anser = await run_tests(logger)
            if anser:
                logger.info("Все тесты пройдены удачно")
            else:
                logger.error("Один из тестов был провален!")
            continue
        
        if menu == 0: # Выход из программы
            return
    
if __name__ == "__main__":
    asyncio.run(main())
