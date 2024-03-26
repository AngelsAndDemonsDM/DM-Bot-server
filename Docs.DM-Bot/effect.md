# Документация по файлу `effect.py`

## `EffectManager.__init__`<br>
Инициализация объекта эффекта.<br>
<br>**Args:**<br>
id (str, optional): Идентификатор эффекта. По умолчанию None.<br>
power (float, optional): Сила эффекта. По умолчанию None.<br>
tick (int, optional): Количество тактов до завершения эффекта. По умолчанию -1.<br>
<br>
Инициализация менеджера эффектов.<br>
Создает пустой список для хранения эффектов.<br>
<br>
## `EffectManager.update`<br>
Обновление состояния эффекта.<br>
<br>**Returns:**<br>
bool: True, если эффект еще активен, False, если эффект завершился.<br>
<br>
Обновление эффектов.<br>
Вызывает метод update() для каждого эффекта в списке.<br>
Если метод update() возвращает False, эффект удаляется из списка.<br>
<br>
## `EffectManager.f_add_effect`<br>
Добавление нового эффекта в список.<br>
<br>**Args:**<br>
new_effect (Effect): Новый эффект для добавления.<br>
<br>
## `EffectManager.add_effect`<br>
Добавление нового эффекта в список, если его effect_id отсутствует.<br>
<br>**Args:**<br>
new_effect (Effect): Новый эффект для добавления.<br>
<br>**Returns:**<br>
bool: True, если эффект был успешно добавлен, в противном случае False.<br>
<br>
## `EffectManager.remove_effect`<br>
Удаление эффекта из списка по его effect_id.<br>
<br>**Args:**<br>
effect_id (str): ID эффекта, который требуется удалить.<br>
<br>**Returns:**<br>
bool: True, если эффект был успешно удален, в противном случае False.<br>
<br>
## `EffectManager.effects`<br>
Получение списка всех эффектов.<br>
<br>**Returns:**<br>
list: Список всех эффектов.<br>
<br>
