from island.core.constants.ban import BanType
from island.models import Error


class BanError(Error):
    error_type: str = "user.banned"
    error_code: BanType
    ban_dur: int
