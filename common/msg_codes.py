from enum import IntEnum


class UserCodes(IntEnum):
    DISCONNECTED = 0
    # should be treated like HTTP 200, data should be an empty string
    SUCCESS = 1
    # data should be a string with reason
    REGISTER_FAILED = 2
    # data should be a string with reason
    LOGIN_FAILED = 3


class ServerCodes(IntEnum):
    DISCONNECTED = 0
    # data should contain plain object {email: (string), password: (string)}
    REGISTER = 1
    # data should contain plain object {email: (string), password: (string)}
    LOGIN = 2
