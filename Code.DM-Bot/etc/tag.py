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
    
    # Get методы
    def get_id(self):
        """
        Получение ID тега.

        Returns:
            id (string): ID тега.
        """
        return self.id

    # Set методы
    def set_id(self, id):
        """
        Установка ID тега.

        Args:
            id (string): ID тега.

        Returns:
            bool: True, если установка прошла успешно, в противном случае False.
        """
        if isinstance(id, (str, int, float)):
            self.id = str(id)
            return True
        
        return False

class TagsManager:
    def _check_tag(self, tag):
        """
        Проверяет, является ли объект тега экземпляром класса Tag.
        
        Args:
            tag (Tag): Объект тега для проверки.
        
        Raises:
            TypeError: Если переданный объект не является экземпляром класса Tag.
        """
        if not isinstance(tag, Tag):
            raise TypeError("Tag in add/rm must be 'Tag' type.")
    
    def _check_array(self, arr_tags):    
        """
        Проверяет, является ли объект массива списка.
        
        Args:
            arr_tags (list): Объект списка для проверки.
        
        Raises:
            TypeError: Если переданный объект не является списком.
        """
        if not isinstance(arr_tags, list):
            raise TypeError("Array tags in add/rm/find/sort must be 'List' type.")
    
    def _check_tag_id(self, tag):
        """
        Проверяет, имеет ли тег непустой идентификатор.
        
        Args:
            tag (Tag): Объект тега для проверки.
        
        Raises:
            ValueError: Если у тега отсутствует идентификатор.
        """
        if tag.get_id() is None:
            raise ValueError("Tag has empty ID.")
    
    def find(self, arr_tags, tag):
        """
        Ищет тег в списке тегов.
        
        Args:
            arr_tags (list): Список тегов для поиска.
            tag (Tag or str or int or float): Тег для поиска. Может быть объектом класса Tag или его идентификатором.
        
        Returns:
            bool: True, если тег найден, в противном случае False.
        
        Raises:
            TypeError: Если переданный тег не является объектом Tag или строкой, числом или числом с плавающей точкой.
        """
        self._check_array(arr_tags)
        if isinstance(tag, Tag):        
            self._check_tag_id(tag)
            tag_id = tag.get_id()
            for t in arr_tags:
                if t.get_id() == tag_id:
                    return True
        elif isinstance(tag, (str, int, float)):
            tag = str(tag)
            for t in arr_tags:
                if t.get_id() == tag:
                    return True
        else:
            raise TypeError("Tag in add/rm/find must be `String` or `Tag' type")

        return False

    def add(self, arr_tags, tag):
        """
        Добавляет тег в список тегов.
        
        Args:
            arr_tags (list): Список тегов, в который нужно добавить тег.
            tag (Tag or str or int or float): Тег для добавления. Может быть объектом класса Tag или его идентификатором.
        
        Returns:
            bool: True, если тег успешно добавлен, в противном случае False.
        
        Raises:
            TypeError: Если переданный тег не является объектом Tag или строкой, числом или числом с плавающей точкой.
        """
        self._check_tag(tag)
        if not self.find(arr_tags, tag):
            arr_tags.append(tag)
            return True
        
        return False
        
    def rm(self, arr_tags, tag):
        """
        Удаляет тег из списка тегов.
        
        Args:
            arr_tags (list): Список тегов, из которого нужно удалить тег.
            tag (Tag or str or int or float): Тег для удаления. Может быть объектом класса Tag или его идентификатором.
        
        Returns:
            bool: True, если тег успешно удален, в противном случае False.
        
        Raises:
            TypeError: Если переданный тег не является объектом Tag или строкой, числом или числом с плавающей точкой.
        """
        self._check_tag(tag)
        if self.find(arr_tags, tag):
            arr_tags.remove(tag)
            return True
        
        return False
        
    def sort_arr(self, arr_tags):
        """
        Сортирует список тегов по их идентификаторам.
        
        Args:
            arr_tags (list): Список тегов для сортировки.
        """
        self._check_array(arr_tags)
        arr_tags.sort(key=lambda x: x.get_id())
