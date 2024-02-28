import asyncio
import os
import shutil

from tests.test_file_work import test_FileWork
from tests.test_tag_system import test_TagData, test_TagsManager


def del_test_folder():
    test_folder_path = os.path.join(os.getcwd(), 'data', 'test')
    if os.path.exists(test_folder_path):
        shutil.rmtree(test_folder_path)
        print("Test folder deleted successfully.")    

async def run_tests():
    """
    Запускает тесты из папки tests.

    Перед запуском тестов проверяет, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.

    После запуска тестов проверяетб, существует ли папка 'test' в папке 'data'.
    Если папка существует, она удаляется.

    Returns:
        bool: True, если все тесты успешно пройдены, в противном случае False.
    """
    del_test_folder()
    
    # Запускаем тесты
    all_tests_passed = True
    all_tests_passed &= await test_FileWork()
    all_tests_passed &= await test_TagData()
    all_tests_passed &= await test_TagsManager()
    
    del_test_folder()
    
    return all_tests_passed


async def main():
    test_result = await run_tests()
    print("All tests passed:", test_result)


if __name__ == "__main__":
    asyncio.run(main())
