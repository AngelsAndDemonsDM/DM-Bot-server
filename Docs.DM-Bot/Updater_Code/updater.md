# Документация по файлу `updater.py`

## `Updater.__init__`<br>
Инициализация объекта класса Updater.<br>
Вызывает конструктор родительского класса ServerInfo и устанавливает текущую версию программы.<br>
<br>
## `Updater.version`<br>
Возвращает текущую версию программы.<br>
<br>
## `Updater.compare_versions`<br>
Сравнивает две версии и возвращает результат сравнения.<br>
<br>**Args:**<br>
version1 (str): Первая версия для сравнения.<br>
version2 (str): Вторая версия для сравнения.<br>
<br>**Returns:**<br>
int: 1, если version1 > version2; -1, если version1 < version2; 0, если version1 == version2.<br>
<br>
## `Updater.is_new_version`<br>
Проверяет, является ли версия на сервере новее текущей.<br>
<br>**Raises:**<br>
ValueError: Если 'version' отсутствует в _info_json.<br>
<br>**Returns:**<br>
bool: True, если есть новая версия; False, если версия актуальна.<br>
<br>
## `Updater.download`<br>
Скачивает файл с сервера.<br>
<br>**Args:**<br>
file_name (str): Имя файла для сохранения.<br>
chunk_size (int): Размер части для скачивания.<br>
retries (int): Количество попыток скачивания.<br>
timeout (int): Время ожидания ответа сервера.<br>
<br>**Raises:**<br>
RequestException: Если скачивание не удалось после всех попыток.<br>
<br>**Returns:**<br>
str: Имя скачанного файла.<br>
<br>
## `Updater.update`<br>
Обновляет программу до новой версии.<br>
Обновляет программу, скачивая архив с сервера, распаковывая его и удаляя старую версию.<br>
<br>
## `Updater.check_file_in_directory`<br>
Проверяет наличие файла в указанной директории.<br>
<br>**Args:**<br>
directory (str): Директория для поиска файла.<br>
filename (str): Имя файла для проверки.<br>
<br>**Returns:**<br>
bool: True, если файл существует; False, если файла нет.<br>
<br>
## `Updater.get_version`<br>
Получает версию программы из указанного файла.<br>
<br>**Args:**<br>
directory (str): Директория, где находится файл.<br>
filename (str): Имя файла, из которого нужно получить версию.<br>
<br>**Returns:**<br>
str: Версия программы, полученная из файла.<br>
<br>
