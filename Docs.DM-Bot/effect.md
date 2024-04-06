# Документация по файлу `effect.py`

## `Effect.__init__`<br>
Инициализация объекта эффекта.<br>
<br>**Args:**<br>
id (str, optional): Идентификатор эффекта. По умолчанию None.<br>
power (float, optional): Сила эффекта. По умолчанию None.<br>
tick (int, optional): Количество тиков до завершения эффекта. По умолчанию -1.<br>
<br>
## `Effect.update`<br>
Обновление состояния эффекта.<br>
<br>**Returns:**<br>
bool: True, если эффект еще активен, False, если эффект завершился.<br>
<br>
