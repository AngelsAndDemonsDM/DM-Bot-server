from etc.file_work import FileWork


class TestFileWork(FileWork):
    def __init__(self):
        super().__init__("test/test_file_work.dat")

async def test_FileWork(logger):
    try:
        class_file_work = FileWork("test/test_file_work.dat")
        if class_file_work is FileWork:
            return False
    except Exception:
        pass

    # Создаем экземпляр класса TestFileWork
    file_work = TestFileWork()
    
    if await file_work.create_file():
        logger.debug("File successfully created.")
    else:
        logger.debug("Failed to create file.")
        return False
    
    # Устанавливаем данные
    file_work.data = {"key": "value"}
    
    # Сохраняем данные
    await file_work.save_data()
    
    # Загружаем данные
    loaded_data = await file_work.load_data()

    # Проверяем, что загруженные данные соответствуют ожидаемым
    if loaded_data == {"key": "value"}:
        logger.debug("FileWork test successful.")
        return True
    else:
        logger.debug("FileWork test failed.")
        return False
