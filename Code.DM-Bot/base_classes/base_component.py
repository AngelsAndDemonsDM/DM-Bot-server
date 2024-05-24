from typing import Any


class Component:
    def __init__(self):
        """Инициализирует базовый объект компонента.
        """
        self.entity = None

    @property
    def owner(self):
        """Возвращает родительскую сущьность для компонента

        Returns:
            Entity: Родительская сущность.
        """
        return self.entity
    
    @owner.setter
    def owner(self, entity) -> None:
        """Устанавливает родительскую сущность для компонента.

        Args:
            entity (Entity): Родительская сущность.
        """
        self.entity = entity

    def update(self) -> None:
        """Обновляет состояние компонента.
        """
        pass
