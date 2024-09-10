from island.core.constants.error import ErrorEnum
from island.core.i18n import _
from island.models import Error


class RecaptchaError(Error):
    error_code: ErrorEnum = ErrorEnum.RECAPTCHA_INVALID
    error_type: str = "recaptcha.invalid"


class RecaptchaVerificationError(RecaptchaError):
    def __init__(self):
        super().__init__(error_description=_("error.recaptcha.verification.failed"))
