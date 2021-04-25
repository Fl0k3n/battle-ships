from enum import Enum


class UserCodes(Enum):
    DISCONNECTED = 0
    # should be treated like HTTP 200, data should be an empty string
    SUCCESS = 1
    # data should be a string with reason
    REGISTER_FAILED = 2
    # data should be a string with reason
    LOGIN_FAILED = 3
    # data should contain original request for which it succedeed, see REGISTER in ServerCodes
    REGISTER_SUCCESS = 4
    # data should contain original request for which it succedeed, see LOGIN in ServerCodes
    LOGIN_SUCCESS = 5


class ServerCodes(Enum):
    DISCONNECTED = 0
    # data should contain plain object {email: (string), password: (string)}
    REGISTER = 1
    # data should contain plain object {email: (string), password: (string)}
    LOGIN = 2
