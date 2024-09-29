from island.core.config import WORLD_ID
from island.entities import Entity


class BaseWorldEntity(Entity):
    __prefix__ = f"worlds.{WORLD_ID}"

class WorldEntity(BaseWorldEntity):
    pass
