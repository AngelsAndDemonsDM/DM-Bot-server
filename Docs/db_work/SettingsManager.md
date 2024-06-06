# Документация по файлу `SettingsManager.py`


## `SettingsManager.__init__`<br>
Инициализирует менеджер настроек.<br>
**Args:**<br>
settings_name (str, optional): Имя файла настроек. Defaults to "main_settings".<br>
Example:<br>
```py
settings_manager = SettingsManager("app_settings")
```
<br>

## `SettingsManager.load_settings`<br>
Загружает настройки из файла.<br>
**Returns:**<br>
dict: Словарь с настройками.<br>
Example:<br>
```py
settings = await settings_manager.load_settings()
print(settings)
```
<br>

## `SettingsManager.save_settings`<br>
Сохраняет настройки в файл.<br>
**Args:**<br>
settings (dict): Словарь с настройками.<br>
Example:<br>
```py
await settings_manager.save_settings({"theme": "dark", "volume": 75})
```
<br>

## `SettingsManager.set_setting`<br>
Устанавливает значение настройки.<br>
**Args:**<br>
key (str): Ключ настройки, поддерживается вложенность через точку (например, "user.preferences.theme").<br>
value (_type_): Значение настройки.<br>
Example:<br>
```py
await settings_manager.set_setting("user.preferences.theme", "dark")
```
<br>

## `SettingsManager.get_setting`<br>
Получает значение настройки.<br>
**Args:**<br>
key (str): Ключ настройки, поддерживается вложенность через точку (например, "user.preferences.theme").<br>
**Returns:**<br>
_type_: Значение настройки или None, если ключ не найден.<br>
Example:<br>
```py
theme = await settings_manager.get_setting("user.preferences.theme")
print(theme)  # "dark"
```
<br>
