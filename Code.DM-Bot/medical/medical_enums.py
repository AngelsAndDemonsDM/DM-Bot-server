from enum import Enum, auto


class GenderEnum(Enum):
    MALE = auto()
    FEMALE = auto()
    OTHER = auto()

class BreastSizeEnum(Enum):
    ZERO = 0
    A = 1
    B = 2
    C = 3
    D = 4
    E = 5
    F = 6
