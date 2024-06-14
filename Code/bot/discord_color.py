class DiscordColorManager:
    DARK_GREY: bytes = 1 << 0
    RED:       bytes = 1 << 1
    GREEN:     bytes = 1 << 2
    YELLOW:    bytes = 1 << 3
    BLUE:      bytes = 1 << 4
    PINK:      bytes = 1 << 5
    TEAL:      bytes = 1 << 6
    WHITE:     bytes = 1 << 7
    
    __slots__ = []
    
    def __init__(self):
        pass

    def get_color(self, text: str, color: bytes):
        if color == DiscordColorManager.DARK_GREY:
            return f"[2;30m{text}[0m"
        
        elif color == DiscordColorManager.RED:
            return f"[2;31m{text}[0m"
        
        elif color == DiscordColorManager.GREEN:
            return f"[2;32m{text}[0m"
        
        elif color == DiscordColorManager.YELLOW:
            return f"[2;33m{text}[0m"
        
        elif color == DiscordColorManager.BLUE:
            return f"[2;34m{text}[0m"
        
        elif color == DiscordColorManager.PINK:
            return f"[2;35m{text}[0m"
        
        elif color == DiscordColorManager.TEAL:
            return f"[2;36m{text}[0m"
        
        elif color == DiscordColorManager.WHITE:
            return f"[2;37m{text}[0m"
