class DiscordColorManager:
    def __init__(self):
        pass

    '''
    0 - тёмно серый
    1 - красный
    2 - зелёный
    3 - жёлтый
    4 - синий
    5 - розовый
    6 - бирюзовый
    7 - белый 
    '''
    def get_color(self, text: str, color: int):
        if color == 0:
            return f"[2;30m{text}[0m"
        elif color == 1:
            return f"[2;31m{text}[0m"
        elif color == 2:
            return f"[2;32m{text}[0m"
        elif color == 3:
            return f"[2;33m{text}[0m"
        elif color == 4:
            return f"[2;34m{text}[0m"
        elif color == 5:
            return f"[2;35m{text}[0m"
        elif color == 6:
            return f"[2;36m{text}[0m"
        elif color == 7:
            return f"[2;37m{text}[0m"
