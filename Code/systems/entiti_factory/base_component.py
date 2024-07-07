from abc import ABC, abstractmethod


class Component(ABC):
    __slots__ = ['owner']

    def __init__(self, owner=None):
        self.owner = owner

    @abstractmethod
    def __repr__(self):
        pass

    @classmethod
    def default_values(cls):
        return {}
