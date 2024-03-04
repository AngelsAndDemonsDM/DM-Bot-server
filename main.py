import asyncio
import os
import shutil

from logger_manager import LoggerManager
from tests.test_file_work import test_FileWork
from tests.test_tag_system import test_TagData, test_TagsManager


def del_test_folder(logger):
    test_folder_path = os.path.join(os.getcwd(), 'data', 'test')
    if os.path.exists(test_folder_path):
        shutil.rmtree(test_folder_path)
        logger.debug("Test folder deleted successfully.")    

async def run_tests(logger):
    """
    Запускает тесты из папки tests.

    Перед запуском тестов проверяет, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.

    После запуска тестов проверяетб, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.

    Returns:
        bool: True, если все тесты успешно пройдены, в противном случае False.
    """
    del_test_folder(logger)
    
    # Запускаем тесты
    all_tests_passed = True
    all_tests_passed &= await test_FileWork(logger)
    all_tests_passed &= await test_TagData(logger)
    all_tests_passed &= await test_TagsManager(logger)
    
    del_test_folder(logger)
    
    return all_tests_passed

def show_menu():
    while True:
        print("\nМеню выбора:")
        print("1. Запуск тестов")
        print("99. Выход")
        choice = input("Введите число: ")
        if choice in {"1", "99"}:
            return int(choice)
        else:
            print("Неверное число. Просьба повторить ввод.")

async def main():
    # Объявление менеджеров
    logger = LoggerManager()
    
    test_result = await run_tests(logger)
    logger.info(f"All tests passed: {test_result}")


    # Меню выбора
    while True:
        menu = show_menu()
        
        if menu == 1: # Запуск тестов
            anser = await run_tests(logger)
            if anser:
                logger.info("Все тесты пройдены удачно")
            else:
                logger.error("Один из тестов был провален!")
        
        if menu == 99: # Выход из программы
            return
    
if __name__ == "__main__":
    asyncio.run(main())
