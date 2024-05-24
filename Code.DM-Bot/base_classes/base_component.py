class Component:
    def __init__(self):
        """Инициализирует базовый объект компонента.
        """
        self.entity = None

    def set_entity(self, entity) -> None:
        """Устанавливает родительскую сущность для компонента.

        Args:
            entity (Entity): Родительская сущность.
        """
        self.entity = entity

    def update(self) -> None:
        """Обновляет состояние компонента.
        """
        pass
