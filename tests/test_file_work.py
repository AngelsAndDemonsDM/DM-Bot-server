import os

from abstract.file_work import FileWork


class TestFileWork(FileWork):
    def __init__(self):
        super().__init__("test/test_file_work.dat")

async def test_FileWork(logger):
    try:
        class_file_work = FileWork("test/test_file_work.dat")
    except Exception as err:
        logger.debug(err)

    # Создаем экземпляр класса TestFileWork
    file_work = TestFileWork()
    
    # Создаем файл и директорию
    await file_work.create_file()
    
    # Проверяем, что файл был создан
    file_path = os.path.join(os.getcwd(), 'data', 'test', 'test_file_work.dat')
    if os.path.exists(file_path):
        logger.debug("File successfully created.")
    else:
        logger.error("Failed to create file.")
        return False
    
    # Устанавливаем данные
    file_work.data = {"key": "value"}
    
    # Сохраняем данные
    await file_work.save_data()
    
    # Загружаем данные
    loaded_data = await file_work.load_data()

    # Проверяем, что загруженные данные соответствуют ожидаемым
    if loaded_data == {"key": "value"}:
        logger.info("FileWork test successful.")
        return True
    else:
        logger.error("FileWork test failed.")
        return False
