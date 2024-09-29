from enum import Enum


class EventEnum(Enum):
    APP_START_EVENT = "app:start"
    APP_STOP_EVENT = "app:stop"
    WORLD_PLAYER_JOIN = "world:player:join"
    WORLD_PLAYER_LEAVE = "world:player:leave"
