# Документация по файлу `auto_docs.py`


## `AutoDocs.extract_docstrings`<br>
Извлекает документационные строки из содержимого файла.<br>
**Args:**<br>
file_content (str): Содержимое файла.<br>
**Returns:**<br>
dict: Словарь, где ключи - имена методов/атрибутов, значения - их документация.<br>
<br>

## `AutoDocs.format_docstring`<br>
Форматирует документацию для отображения в файле Markdown.<br>
**Args:**<br>
name (str): Имя метода/атрибута.<br>
docstring (str или list): Документация, представленная в виде строки или списка строк.<br>
**Returns:**<br>
str: Отформатированная документация.<br>
<br>

## `AutoDocs.generate_documentation`<br>
Генерирует документацию по файлам в указанной папке.<br>
<br>
