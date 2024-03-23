from typing import Union


class Tag:
    def __init__(self, id: str):
        """
        Инициализация объекта Tag.

        Args:
            id (str): Идентификатор тега.
        """
        self._id = id
    
    def __str__(self):
        """
        Возвращает строковое представление тега.

        Returns:
            str: Строковое представление тега.
        """
        return self._id

    # Get методы
    @property
    def id(self):
        """
        Получение ID тега.

        Returns:
            str: ID тега.
        """
        return self._id

    # Set методы
    @id.setter
    def id(self, id: Union[str, int, float]):
        """
        Установка ID тега.

        Args:
            id (str, int, float): Новый идентификатор тега.
        """
        self._id = str(id)

class TagsManager:
    def find(self, arr_tags: list, tag: str):
        """
        Ищет тег в списке тегов.

        Args:
            arr_tags (list): Список тегов для поиска.
            tag (str): Тег для поиска.

        Returns:
            bool: True, если тег найден, в противном случае False.
        """
        for t in arr_tags:
            if str(t) == tag:
                return True
        
        return False

    def add(self, arr_tags: list, tag: Tag):
        """
        Добавляет тег в список тегов.

        Args:
            arr_tags (list): Список тегов, в который нужно добавить тег.
            tag (Tag): Тег для добавления.

        Returns:
            bool: True, если тег успешно добавлен, в противном случае False.
        """
        if tag not in arr_tags:
            arr_tags.append(tag)
            return True
        
        return False
        
    def remove(self, arr_tags: list, tag: Tag):
        """
        Удаляет тег из списка тегов.

        Args:
            arr_tags (list): Список тегов, из которого нужно удалить тег.
            tag (Tag): Тег для удаления.

        Returns:
            bool: True, если тег успешно удален, в противном случае False.
        """
        if tag in arr_tags:
            arr_tags.remove(tag)
            return True
        
        return False
        
    def sort_arr(self, arr_tags: list):
        """
        Сортирует список тегов по их идентификаторам.

        Args:
            arr_tags (list): Список тегов для сортировки.
        """
        arr_tags.sort(key=lambda x: x.id)
