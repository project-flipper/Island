from enum import IntEnum


class CloseCode(IntEnum):
    NORMAL = 1000
    INVALID_DATA = 1003
    # Auth
    AUTHENTICATION_FAILED = 4000
    AUTHENTICATION_TIMEOUT = 4001
