# Документация по файлу `effect.py`

## `EffectManager.__init__`<br>
<br>
Инициализация объекта эффекта.<br>
<br>
**Args:**<br>
effect_id (str, optional): Идентификатор эффекта. По умолчанию None.<br>
power (float, optional): Сила эффекта. По умолчанию None.<br>
tick (int, optional): Количество тактов до завершения эффекта. По умолчанию -1.<br>
<br>
<br>
Инициализация менеджера эффектов.<br>
<br>
Создает пустой список для хранения эффектов.<br>
<br>
<br>
## `EffectManager.update`<br>
<br>
Обновление состояния эффекта.<br>
<br>
**Returns:**<br>
bool: True, если эффект еще активен, False, если эффект завершился.<br>
<br>
<br>
Обновление эффектов.<br>
<br>
Вызывает метод update() для каждого эффекта в списке.<br>
Если метод update() возвращает False, эффект удаляется из списка.<br>
<br>
<br>
## `EffectManager.set_effect_id`<br>
<br>
Установка идентификатора эффекта.<br>
<br>
**Args:**<br>
new_effect_id (str, int, float): Новый идентификатор эффекта.<br>
<br>
<br>
## `EffectManager.set_strength`<br>
<br>
Установка силы эффекта.<br>
<br>
**Args:**<br>
new_strength (int, float): Новое значение силы эффекта.<br>
<br>
<br>
## `EffectManager.set_tick`<br>
<br>
Установка количества тактов до завершения эффекта.<br>
<br>
**Args:**<br>
new_tick (int): Новое количество тактов до завершения эффекта.<br>
<br>
**Returns:**<br>
bool: True, если установка прошла успешно, в противном случае False.<br>
<br>
<br>
## `EffectManager.get_tick`<br>
<br>
Получение количества тактов до завершения эффекта.<br>
<br>
**Returns:**<br>
int: Количество тактов до завершения эффекта.<br>
<br>
<br>
## `EffectManager.get_effect_id`<br>
<br>
Получение идентификатора эффекта.<br>
<br>
**Returns:**<br>
str: Идентификатор эффекта.<br>
<br>
<br>
## `EffectManager.get_strength`<br>
<br>
Получение силы эффекта.<br>
<br>
**Returns:**<br>
float: Сила эффекта.<br>
<br>
<br>
## `EffectManager.get_cur_effect`<br>
<br>
Получение текущего состояния эффекта в виде списка.<br>
<br>
**Returns:**<br>
list: [effect_id, strength], текущее состояние эффекта.<br>
<br>
<br>
## `EffectManager.f_add_effect`<br>
<br>
Добавление нового эффекта в список.<br>
<br>
**Args:**<br>
new_effect (Effect): Новый эффект для добавления.<br>
<br>
<br>
## `EffectManager.add_effect`<br>
<br>
Добавление нового эффекта в список, если его effect_id отсутствует.<br>
<br>
**Args:**<br>
new_effect (Effect): Новый эффект для добавления.<br>
<br>
**Returns:**<br>
bool: True, если эффект был успешно добавлен, в противном случае False.<br>
<br>
<br>
## `EffectManager.remove_effect`<br>
<br>
Удаление эффекта из списка по его effect_id.<br>
<br>
**Args:**<br>
effect_id (str): ID эффекта, который требуется удалить.<br>
<br>
**Returns:**<br>
bool: True, если эффект был успешно удален, в противном случае False.<br>
<br>
<br>
## `EffectManager.get_all_effects`<br>
<br>
Получение списка всех эффектов.<br>
<br>
**Returns:**<br>
list: Список всех эффектов.<br>
<br>
<br>
## `EffectManager.get_all_effects_in_list`<br>
<br>
Получение списка, содержащего информацию о каждом эффекте в формате [effect_id, strength].<br>
<br>
**Returns:**<br>
list: Список, содержащий информацию о каждом эффекте.<br>
<br>
<br>
