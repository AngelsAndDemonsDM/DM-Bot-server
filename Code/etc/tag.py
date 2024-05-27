class TagsManager:
    def __init__(self):
        """
        Инициализирует новый объект TagsManager.

        Attributes:
            _ids (list): List ID.
        """
        self._ids = []

    def find(self, id: str) -> bool:
        """
        Проверяет, существует ли id ID в списке ID.

        Args:
            id (str): Id, который нужно проверить.

        Returns:
            bool: True если ID существует, False в противном случае.
        """
        for t in self._ids:
            if t == id:
                return True
        return False

    def add(self, id: str) -> bool:
        """
        Добавляет новый ID в список ID.

        Args:
            id (str): ID, который нужно добавить.

        Returns:
            bool: True если ID был добавлен, False в противном случае
        """
        if id not in self._ids:
            self._ids.append(id)
            return True
        return False

    def remove(self, id: id) -> bool:
        """
        Удаляет ID из списка ID.

        Args:
            id (str): ID, который нужно удалить.

        Returns:
            bool: True если ID был удален, False в противном случае.
        """
        if id in self._ids:
            self._ids.remove(id)
            return True
        return False

    def sort(self) -> None:
        """
        Сортирует list ID в алфавитном порядке.
        """
        self._ids = sorted(self._ids)
