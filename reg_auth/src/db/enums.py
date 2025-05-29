from enum import Enum

class RoleEnum(str, Enum):
    LISTNER = "LISTNER"
    ARTIST = "ARTIST"
    ADMIN = "ADMIN"