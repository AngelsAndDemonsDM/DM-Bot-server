# Документация по файлу `file_work.py`

## `FileWork.__init__`<br>
<br>
Инициализация объекта FileWork.<br>
<br>
**Args:**<br>
file_path (str): Путь к файлу.<br>
<br>
**Attributes:**<br>
path (str): Полный путь к файлу.<br>
data (object): Данные файла.<br>
cached (bool): Флаг указывающий, кэшированы ли данные.<br>
file_hash (str): Хэш файла.<br>
lock (asyncio.Lock): Асинхронный замок для обеспечения безопасности при доступе к данным из разных потоков.<br>
<br>
<br>
## `FileWork.__new__`<br>
<br>
Метод для создания экземпляра класса.<br>
<br>
**Raises:**<br>
NotImplementedError: Вызывается, если пытаются создать экземпляр абстрактного класса FileWork.<br>
<br>
<br>
## `FileWork.create_file`<br>
<br>
Создание директории и файла, если они не были созданы ранее.<br>
<br>
**Returns:**<br>
bool: Возвращает True если файл был создан, иначе False<br>
<br>
<br>
## `FileWork.load_data`<br>
<br>
Загрузка данных с использованием кэширования и проверки хеша файла.<br>
<br>
**Returns:**<br>
object: Загруженные данные файла.<br>
<br>
<br>
## `FileWork.save_data`<br>
<br>
Сохранение данных.<br>
<br>
<br>
## `FileWork.data`<br>
<br>
Возвращает текущие данные класса<br>
<br>
**Returns:**<br>
any: Данные, записанные в классе<br>
<br>
<br>
Записывает в data класса кастомные данные<br>
<br>
**Args:**<br>
data (any): Данные для записи в класс<br>
<br>
<br>
