from enum import Enum


class Event(Enum):
    MOUSE_ENTERED = 0      # when mouse enters cell
    MOUSE_LEFT = 1         # mouse leaves cell
    CELL_CLICKED = 2
    REGISTER = 3           # passing email + password as data
    LOGIN = 4              # passing email + password as data
    JOIN_ROOM = 5          # data is room id
    CREATE_ROOM = 6
    REFRESH_ROOMS = 7
    # data is List[(old_i, old_j), (new_i, new_j), (beaten_i, beaten_j), last_move?]
    # where (beaten_i, beaten_j) should be -1, -1 if nothing was beaten last_move should be true or false
    PLAYER_MOVED = 8
