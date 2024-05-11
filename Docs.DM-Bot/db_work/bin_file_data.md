# Документация по файлу `bin_file_data.py`


## `BinFileData.__init__`<br>
Инициализация объекта BinFileData.<br>
**Args:**<br>
file_path (str): Путь к файлу.<br>
**Examples:**<br>
Создание экземпляра класса BinFileData для работы с файлом "example_data.bin"<br>
```py
file_data = BinFileData("example_data")
```
<br>

## `BinFileData.load_data`<br>
Загрузка данных с использованием кэширования и проверки хеша файла.<br>
**Returns:**<br>
object: Загруженные данные файла.<br>
**Raises:**<br>
FileNotFoundError: Если файл не найден.<br>
**Examples:**<br>
Загрузка данных из файла "example_data.bin"<br>
```py
loaded_data = file_data.load_data()
print("Загруженные данные из файла:", loaded_data)
```
<br>

## `BinFileData.save_data`<br>
Сохранение данных.<br>
**Examples:**<br>
Сохранение данных в файл "example_data.bin"<br>
```py
file_data.save_data()
```
<br>

## `BinFileData.data`<br>
Возвращает или записывает данные<br>
**Returns:**<br>
any: Данные, записанные в классе<br>
**Examples:**<br>
Получение данных из объекта класса<br>
```py
file_data = BinFileData("example_data")
file_data.data = 123
file_data.save_data()
file_data.data = 124
file_data.load_data()
print("Данные из объекта класса:", file_data.data)
```
print выведет `Данные из объекта класса: 123`<br>
<br>
