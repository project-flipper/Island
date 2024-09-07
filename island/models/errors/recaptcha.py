from island.core.constants.error import ErrorEnum
from island.models import Error


class RecaptchaError(Error):
    error_code: ErrorEnum = ErrorEnum.RECAPTCHA_INVALID
    error_type = "recaptcha.invalid"
