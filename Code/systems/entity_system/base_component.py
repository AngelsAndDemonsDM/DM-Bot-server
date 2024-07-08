from abc import ABC, abstractmethod
from typing import Any, Dict, Type


class BaseComponent(ABC):
    __slots__ = ['comp_type', 'owner']
    
    def __init__(self, comp_type: str = "BaseComponent") -> None:
        self.comp_type: str = comp_type
        self.owner: 'BaseEntity' = None  # type: ignore

    @abstractmethod
    def __repr__(self) -> str:
        """
        Этот метод служит для предоставления строкового представления компонента.
        Необходимо переопределить этот метод в подклассах, чтобы возвращать строку,
        содержащую имя класса и параметры его конструктора.
        
        Например, для базового класса это может выглядеть так:
        ```python
        return f"BaseComponent(comp_type={self.comp_type})"
        ```
        """
        pass

    @staticmethod
    @abstractmethod
    def get_type_hints() -> Dict[str, Type[Any]]:
        """
        Этот статический метод возвращает словарь с именами переменных и их типами.
        Необходимо переопределить этот метод в подклассах, чтобы возвращать корректные типы
        для каждого атрибута компонента.
        
        Например, для HealthComponent это может выглядеть так:
        ```python
        return {'hp': int, 'regen': int}
        ```
        """
        pass
