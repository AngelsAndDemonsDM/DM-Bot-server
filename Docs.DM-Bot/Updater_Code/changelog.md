# Документация по файлу `changelog.py`

## `Changelog.__init__`<br>
Инициализация объекта класса Changelog.<br>
Вызывает конструктор родительского класса ServerInfo.<br>
<br>
## `Changelog.get_changelog`<br>
Получает changelog с сервера и возвращает его в формате словаря.<br>
<br>**Raises:**<br>
ValueError: Если 'changelog_id' отсутствует в _info_json.<br>
RequestException: Если возникает ошибка при загрузке changelog.<br>
<br>**Returns:**<br>
dict: Словарь с информацией из changelog.<br>
<br>
## `Changelog.print_changelog`<br>
Выводит changelog на экран, разбивая на страницы по 10 версий.<br>
Выводит информацию о версиях, датах и изменениях в формате:<br>
Версия: [version]<br>
Дата: [date]<br>
Изменения:<br>
- [change1]<br>
- [change2]<br>
...<br>
Если changelog отсутствует или пользователь решит не продолжать просмотр,<br>
выводится соответствующее сообщение.<br>
<br>
