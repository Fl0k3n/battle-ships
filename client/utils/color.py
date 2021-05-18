from enum import Enum


class Color(Enum):
    WHITE = 0,
    BLACK = 1,

    @classmethod
    def reverse(cls, color):
        return cls.BLACK if color == cls.WHITE else cls.WHITE
