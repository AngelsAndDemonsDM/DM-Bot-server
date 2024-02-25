import os
import pickle

from abstract.file_work import FileWork


class TestFileWork(FileWork):
    def __init__(self):
        super().__init__("test/test_file_work.dat")

async def TestFileWorkDef():
    try:
        class_file_work_d = FileWork("test/test_file_work.dat")
    except Exception as err:
        print(err)
    
    class_file_work = TestFileWork()
    await class_file_work.create_file()    
    class_file_work.data = {"key": "value"}
    await class_file_work.save_data()
    
    loaded_data = await class_file_work.load_data()
    print(loaded_data)
    
    return True
