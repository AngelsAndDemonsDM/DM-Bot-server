# Документация по файлу `SettingsManager.py`


## `SettingsManager.load_settings`<br>
Загрузка настроек из файла.<br>
**Returns:**<br>
dict: Словарь с настройками<br>
<br>

## `SettingsManager.save_settings`<br>
Сохранение настроек в файл.<br>
**Args:**<br>
settings (dict): Словарь с настройками<br>
<br>

## `SettingsManager.set_setting`<br>
Устанавливает значение определенного поля в файле настроек.<br>
**Args:**<br>
key (str): Ключ поля<br>
value: Значение поля<br>
<br>

## `SettingsManager.get_setting`<br>
Получает значение определенного поля из файла настроек.<br>
**Args:**<br>
key (str): Ключ поля<br>
**Returns:**<br>
Значение поля или None, если ключ не найден<br>
<br>
