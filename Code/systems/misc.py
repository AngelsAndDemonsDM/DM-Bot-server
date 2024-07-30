from typing import Any


class GlobalClass:
    _instance: Any = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GlobalClass, cls).__new__(cls)
        
        return cls._instance

    # Данную дичь прописывать в каждом глобальном классе. И мне похуй
    #def __init__(self, *args, **kwargs):
    #    if not hasattr(self, '_initialized'):
    #        self._initialized = True
