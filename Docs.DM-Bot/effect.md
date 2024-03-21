# Документация по файлу effect

## `update`<br>
Обновление эффектов.<br>
<br>
Вызывает метод update() для каждого эффекта в списке.<br>
Если метод update() возвращает False, эффект удаляется из списка.<br>
<br>
## `get_tick`<br>
Получение количества тактов до завершения эффекта.<br>
<br>
**Returns:**<br>
int: Количество тактов до завершения эффекта.<br>
<br>
## `get_effect_id`<br>
Получение идентификатора эффекта.<br>
<br>
**Returns:**<br>
str: Идентификатор эффекта.<br>
<br>
## `get_strength`<br>
Получение силы эффекта.<br>
<br>
**Returns:**<br>
float: Сила эффекта.<br>
<br>
## `get_cur_effect`<br>
Получение текущего состояния эффекта в виде списка.<br>
<br>
**Returns:**<br>
list: [effect_id, strength], текущее состояние эффекта.<br>
<br>
## `__init__`<br>
Инициализация менеджера эффектов.<br>
<br>
Создает пустой список для хранения эффектов.<br>
<br>
## `get_all_effects`<br>
Получение списка всех эффектов.<br>
<br>
**Returns:**<br>
list: Список всех эффектов.<br>
<br>
## `get_all_effects_in_list`<br>
Получение списка, содержащего информацию о каждом эффекте в формате [effect_id, strength].<br>
<br>
**Returns:**<br>
list: Список, содержащий информацию о каждом эффекте.<br>
<br>