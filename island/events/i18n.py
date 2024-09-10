import i18n
from fastapi_events.handlers.local import local_handler
from fastapi_events.typing import Event
from loguru import logger

from island.core.config import I18N_DIR
from island.core.constants.events import EventEnum
from island.core.i18n import _


@local_handler.register(event_name=str(EventEnum.APP_START_EVENT))
async def setup_i18n(event: Event):
    i18n.set("filename_format", "{locale}.{format}")
    i18n.load_path.append(I18N_DIR)

    island_info = _("island_info", locale="en")
    check = island_info == "Island server"
    logger.info(
        "i18n test: island_info (en): {}, equals to 'Island server': {}",
        island_info,
        check,
    )

    if not check:
        logger.warning("I18N setup failed. i18n keys won't be translated.")
