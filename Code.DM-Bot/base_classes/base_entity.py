from typing import Dict, Optional

from base_classes.base_component import Component


class Entity:
    def __init__(self, name: str):
        """Инициализирует объект сущности.

        Args:
            name (str): Имя сущности.
        """
        self.name: str = name
        self.components: Dict[str, Dict[str, Component]] = {}

    def add_component(self, component_type: str, component_id: str, component: Component) -> None:
        """Добавляет компонент к сущности.

        Args:
            component_type (str): Тип компонента.
            component_id (str): Идентификатор компонента.
            component (Component): Объект компонента.
        """
        component.set_entity(self)
        if component_type not in self.components:
            self.components[component_type] = {}
        self.components[component_type][component_id] = component

    def get_component(self, component_type: str, component_id: str) -> Optional[Component]:
        """Возвращает компонент по его типу и идентификатору.

        Args:
            component_type (str): Тип компонента.
            component_id (str): Идентификатор компонента.

        Returns:
            Optional[Component]: Объект компонента, если найден, иначе None.
        """
        return self.components.get(component_type, {}).get(component_id)

    def update(self) -> None:
        """Обновляет все компоненты сущности.
        """
        for component_dict in self.components.values():
            for component in component_dict.values():
                component.update()
