

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
    