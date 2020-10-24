from enum import Enum

class Scope(Enum):
    Master      = "master"

    UserDev     = "user:dev"
    UserRead    = "user:read"
    UserWrite   = "user:write"
    UserCreate  = "user:create"
    UserLogin   = "user:login"
    UserAuth    = "user:auth"

    WorldAccess = "world:access"
    WorldDev    = "world:dev"
    