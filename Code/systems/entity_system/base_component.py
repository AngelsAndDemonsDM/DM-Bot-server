from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, Type


class BaseComponent(ABC):
    __slots__ = ['comp_type', 'owner']
    
    def __init__(self, comp_type: str = "BaseComponent") -> None:
        """Инициализирует базовый компонент с заданным типом компонента.

        Args:
            comp_type (str, optional): Тип компонента. По умолчанию "BaseComponent".
        """
        self.comp_type: str = comp_type
        self.owner: 'BaseEntity' = None  # type: ignore

    def get_owner(self) -> Optional['BaseEntity']: # type: ignore
        """Возвращает владельца компонента, если он существует.

        Returns:
            Optional[BaseEntity]: Владелец компонента, если он существует, иначе None.
        """
        return self.owner
    
    @abstractmethod
    def __repr__(self) -> str:
        """Возвращает строковое представление компонента. Этот метод должен быть переопределен в подклассах, чтобы возвращать строку, содержащую имя класса и параметры его конструктора.

        Returns:
            str: Строковое представление компонента.
        
        Например, для базового класса это может выглядеть так::
            
            return f"BaseComponent(comp_type={self.comp_type})"
        """
        pass

    @staticmethod
    @abstractmethod
    def get_type_hints() -> Dict[str, Type[Any]]:
        """Возвращает словарь с именами переменных и их типами. Этот метод должен быть переопределен в подклассах, чтобы возвращать корректные типы для каждого атрибута компонента.

        Returns:
            Dict[str, Type[Any]]: Словарь с именами переменных и их типами.
        
        Например, для HealthComponent это может выглядеть так::
        
            return {'hp': int, 'regen': int}
        """
        pass
