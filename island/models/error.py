from island.models import Error
from island.core.constants.ban import BanType


class BanError(Error):
    error_type = "user.banned"
    error_code: BanType
    ban_dur: int
