from httpx import AsyncClient, HTTPError

from island.core.config import (
    GOOGLE_RECAPTCHA_V3_SECRET,
    IS_DEVELOPMENT_MODE,
    SKIP_RECAPTCHA_ON_DEVELOPMENT,
)
from island.core.constants.urls import URLConstantsEnum


async def verify_google_recaptcha(token: str, /) -> bool:
    """Verify the given google recaptcha v3 token

    :param token: Google reCaptcha v3 response token
    :type token: str
    :return: True if the token is verified else False
    :rtype: bool
    """

    if IS_DEVELOPMENT_MODE and SKIP_RECAPTCHA_ON_DEVELOPMENT:
        return True

    data = {"secret": GOOGLE_RECAPTCHA_V3_SECRET, "response": token}
    async with AsyncClient() as client:
        try:
            r = await client.post(
                str(URLConstantsEnum.GOOGLE_RECAPTCHA_V3_VERIFY_ENDPOINT), data=data
            )
            return r.is_success
        except Exception:
            return False
