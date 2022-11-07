import enum

@enum.unique
class TileStatus(enum.IntEnum):
    EMPTY   = 0
    HOSTILE = 1
    ALLIED  = 2
    BLOCKED = 3
    PLAYER  = 4