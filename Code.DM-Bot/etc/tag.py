from typing import Union


class Tag:
    def __init__(self, id=None):
        """
        Инициализация объекта Tag.

        Args:
            id (string, optional): Идентификатор тега. По умолчанию None.
        
        Raises:
            TypeError: Если тип переданного идентификатора не поддерживается.
        """
        if id is None:
            self.id = None
        elif not self.set_id(id):
            raise TypeError(f"Tag id in {self.__class__.__name__}. must be a `string` type.")
    
    def __str__(self):
        return self.id

    # Get методы
    @property
    def id(self):
        """
        Получение ID тега.

        Returns:
            id (string): ID тега.
        """
        return self.id

    # Set методы
    @id.setter
    def set_id(self, id: Union[str, int, float]):
        """
        Установка ID тега.

        Args:
            id (string): ID тега.
        """
        self.id = str(id)

class TagsManager:
    def find(self, arr_tags: list, tag: str):
        """
        Ищет тег в списке тегов.
        
        Args:
            arr_tags (list): Список тегов для поиска.
            tag (Tag or str or int or float): Тег для поиска. Может быть объектом класса Tag или его идентификатором.
        
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
            tag (Tag or str or int or float): Тег для добавления. Может быть объектом класса Tag или его идентификатором.
        """
        if not self.find(arr_tags, tag):
            arr_tags.append(tag)
            return True
        
        return False
        
    def remove(self, arr_tags: list, tag: Tag):
        """
        Удаляет тег из списка тегов.
        
        Args:
            arr_tags (list): Список тегов, из которого нужно удалить тег.
            tag (Tag or str or int or float): Тег для удаления. Может быть объектом класса Tag или его идентификатором.
        
        Returns:
            bool: True, если тег успешно удален, в противном случае False.
        """
        if self.find(arr_tags, tag):
            arr_tags.remove(tag)
            return True
        
        return False
        
    def sort_arr(self, arr_tags: list):
        """
        Сортирует список тегов по их идентификаторам.
        
        Args:
            arr_tags (list): Список тегов для сортировки.
        """
        arr_tags.sort(key=lambda x: x.get_id())
