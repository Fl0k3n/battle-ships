from enum import Enum


class Event(Enum):
    MOUSE_ENTERED = 0  # when mouse enters cell
    MOUSE_LEFT = 1  # mouse leaves cell
    CELL_CLICKED = 2
