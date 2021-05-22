from enum import Enum


class UserCodes(Enum):
    # no data
    DISCONNECTED = 0
    # multipurpose code for internal server errors, data should be a string with reason
    ERROR = 1
    # should be treated like HTTP 200, data should be an empty string
    SUCCESS = 2
    # data should be a string with reason
    REGISTER_FAILED = 3
    # data should be a string with reason
    LOGIN_FAILED = 4
    # data should contain original request for which it succedeed, see REGISTER in ServerCodes
    REGISTER_SUCCESS = 5
    # data should contain original request for which it succedeed, see LOGIN in ServerCodes
    LOGIN_SUCCESS = 6
    # data should be {room_id: (int)}
    ROOM_CREATED = 7
    # data should contain list of rooms, see server/room.py/get_formatted_data for format
    ROOMS_FETCHED = 8
    # data should be {room_id: (int)}, sent to user joining room
    JOINED_ROOM = 9
    # data should be {email: (guest email)}, sent to owner waiting for sb to join his room
    GUEST_JOINED_ROOM = 10
    # data should be a string with reason
    FAILED_TO_JOIN_ROOM = 11
    # data should contain move data, see PLAYER_MOVED in client/utils/events
    PLAYER_MOVED = 12
    # data should be an empty string, should be detected when one user waits for others move
    ENEMY_DISCONNECTED = 13
    # data should be an empty string
    ROOM_LEFT = 14


class ServerCodes(Enum):
    # no data
    DISCONNECTED = 0
    # data should contain plain object {email: (string), password: (string)}
    REGISTER = 1
    # data should contain plain object {email: (string), password: (string)}
    LOGIN = 2
    # data should be an empty string
    CREATE_ROOM = 3
    # data should be an empty string
    GET_ROOMS = 4
    # data should be {room_id: (int)}
    JOIN_ROOM = 5
    # data should be {room_id: (int), move_data: Any}, for move_data see PLAYER_MOVED in client/utils/events
    PLAYER_MOVED = 6
    # data should be empty string
    LEAVE_ROOM = 7
