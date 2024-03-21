from enum import enum, auto


class DiscordColor(enum):
    """
        0 - тёмно серый
        1 - красный
        2 - зелёный
        3 - жёлтый
        4 - синий
        5 - розовый
        6 - бирюзовый
        7 - белый 
    """
    DARK_GREY = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()
    BLUE = auto()
    PINK = auto()
    TEAL = auto()
    WHITE = auto()

class DiscordColorManager:
    def __init__(self):
        pass

    def get_color(self, text: str, color: DiscordColor):
        if color == DiscordColor.DARK_GREY:
            return f"[2;30m{text}[0m"
        elif color == DiscordColor.RED:
            return f"[2;31m{text}[0m"
        elif color == DiscordColor.GREEN:
            return f"[2;32m{text}[0m"
        elif color == DiscordColor.YELLOW:
            return f"[2;33m{text}[0m"
        elif color == DiscordColor.BLUE:
            return f"[2;34m{text}[0m"
        elif color == DiscordColor.PINK:
            return f"[2;35m{text}[0m"
        elif color == DiscordColor.TEAL:
            return f"[2;36m{text}[0m"
        elif color == DiscordColor.WHITE:
            return f"[2;37m{text}[0m"
