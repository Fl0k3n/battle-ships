from enum import Enum


class Color(Enum):
    WHITE = 0,
    BLACK = 1,

    @classmethod
    def reverse(cls, color):
        if color == cls.WHITE:
            return cls.BLACK
        return cls.WHITE
