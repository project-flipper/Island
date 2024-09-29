from enum import Enum


class EventEnum(Enum):
    APP_START_EVENT = "app:start"
    APP_STOP_EVENT = "app:stop"
    WORLD_CLIENT_CONNECT = "world:client:connect"
    WORLD_CLIENT_AUTH = "world:client:auth"
    WORLD_CLIENT_DISCONNECT = "world:client:disconnect"
