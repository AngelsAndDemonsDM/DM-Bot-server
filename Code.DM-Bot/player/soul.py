import pickle


class PlayerSoul:
    def __init__(self, discord_id: int, discord_name: str) -> None:
        self._id: int = discord_id
        self._name: str = discord_name

    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    def serialized(self) -> bytes:
        return pickle.dumps(self)

    def deserialized(self, blob: bytes) -> None:
        obj: 'PlayerSoul' = pickle.loads(blob) # Явно указываем тип возвращаемого объекта
        self._id = obj._id
        self._name = obj._name
