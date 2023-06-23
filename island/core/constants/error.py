from enum import Enum, auto


class ErrorEnum(Enum):
    RECAPTCHA_INVALID = auto()

    # Ban Types
    MANUAL_BAN = auto()
    AUTO_BAN = auto()
    CHEATING_BAN = auto()
