from enum import IntEnum

from island.core.constants.error import ErrorEnum


class BanType(IntEnum):
    MANUAL_BAN = ErrorEnum.MANUAL_BAN.value
    AUTO_BAN = ErrorEnum.AUTO_BAN.value
    CHEATING_BAN = ErrorEnum.CHEATING_BAN.value
