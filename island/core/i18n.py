from typing import Any
from i18n import t as translate
from starlette_context import context

from island.core.config import I18N_DEFAULT_LOCALE


def _(key: Any, locale=None, **kwargs: Any) -> str | Any:
    locale = locale or context.get("locale", I18N_DEFAULT_LOCALE)
    return translate(key, locale=locale, **kwargs)
