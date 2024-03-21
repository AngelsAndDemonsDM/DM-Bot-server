# Документация по файлу `observer.py`

## `__init__`<br>
Инициализация нового экземпляра класса Observer.<br>
<br>
## `attach`<br>
Подписывает функцию на события.<br>
<br>
**Args:**<br>
func (callable): Функция-подписчик.<br>
remaining (int): Количество уведомлений, которые должен получить подписчик (по умолчанию бесконечное количество).<br>
<br>
## `detach`<br>
Отписывает функцию от событий.<br>
<br>
**Args:**<br>
func (callable): Функция-подписчик.<br>
<br>
## `notify`<br>
Оповещает всех подписчиков о событии.<br>
<br>
**Args:**<br>
args: Позиционные аргументы для передачи подписчикам.<br>
kwargs: Именованные аргументы для передачи подписчикам.<br>
<br>